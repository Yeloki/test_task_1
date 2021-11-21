from hashlib import sha256

from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import serializers

from secureT.settings import SECRET_KEY, EMAIL_HOST_USER, VERIFICATION_LINK
from .models import Post, Comment, User, CompleteRegistrationLink


class FilterCommentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = CommentListSerializer(value, context=self.context)
        return serializer.data


class CommentListSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = Comment
        fields = ('id', 'user', 'body', 'children')


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('body', 'post', 'parent')


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('body',)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'body', 'publication_time')


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('body',)


class PostsSerializer(serializers.ModelSerializer):
    comments = CommentListSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'body', 'publication_time', 'comments')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'date_joined')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=False
        )
        user.set_password(validated_data['password'])
        key = sha256((get_random_string(length=32) + SECRET_KEY + user.email).encode('utf-8')).hexdigest()
        user.save()
        CompleteRegistrationLink.objects.create(
            user=user,
            link=key
        )
        status = send_mail('Подтверждение аккаунта',
                           f'Для подтверждения аккаунта перейдите по этой ссылке: {VERIFICATION_LINK}{key}',
                           EMAIL_HOST_USER,
                           [user.email, ],
                           fail_silently=False)
        return validated_data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password')

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        if 'first_name' in validated_data:
            instance.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            instance.last_name = validated_data['last_name']
        instance.save()
        return instance
