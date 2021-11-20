from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, User, Comment
from django.shortcuts import render
from .serializers import PostsSerializer, PostCreateSerializer
from .serializers import CommentSerializer, CommentCreateSerializer
from .serializers import UsersSerializer


def docs(request):
    return render(request, 'docs.html')


class PostListView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostsSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_anonymous:
            post = PostCreateSerializer(data=request.data)
            if post.is_valid():
                post.validated_data['user'] = request.user
                post.save()
                return Response(status=201)
            return Response(status=400)
        return Response(status=403)


class PostView(APIView):
    def get(self, request, pk):
        obj = Post.objects.filter(id=pk).first()
        if obj is not None:
            serializer = PostsSerializer(obj)
            return Response(serializer.data)
        return Response(status=404)

    def delete(self, request, pk):
        obj = Post.objects.filter(id=pk).first()
        if obj is None:
            return Response(status=404)
        if request.user.is_staff or request.user == obj.user:
            obj.delete()
            return Response(status=202)
        return Response(status=403)

    def put(self, request, pk):
        obj = Post.objects.filter(id=pk).first()
        if obj is None:
            return Response(status=404)
        if request.user.is_staff or obj.user == request.user:
            updated = PostsSerializer(obj, data=request.data, partial=True)
            print(obj.body)
            if updated.is_valid():
                if 'user' not in updated.validated_data:
                    updated.save()
                    return Response(status=202)
            return Response(status=400)
        return Response(status=403)


class CommentCreateView(APIView):
    def post(self, request):
        if not request.user.is_anonymous:
            comment = CommentCreateSerializer(data=request.data)
            if comment.is_valid():
                comment.validated_data['user'] = request.user
                comment.save()
                return Response(status=201)
            return Response(status=400)
        return Response(status=403)


class CommentView(APIView):
    def get(self, request, pk):
        obj = Comment.objects.filter(id=pk).first()
        if obj is not None:
            return Response(CommentSerializer(obj).data)
        return Response(status=404)

    def put(self, request, pk):
        obj = Comment.objects.filter(id=pk).first()
        if obj is None:
            return Response(status=404)
        if request.user.is_staff or obj.user == request.user:
            updated = CommentSerializer(obj, data=request.data, partial=True)
            if not updated.is_valid():
                return Response(status=400)
            if 'post' not in updated.validated_data and 'user' not in updated.validated_data:
                updated.save()
                return Response(status=202)
        return Response(status=403)

    def delete(self, request, pk):
        obj = Comment.objects.filter(id=pk).first()
        if obj is None:
            return Response(status=404)
        if request.user.is_staff or request.user == obj.user:
            obj.delete()
            return Response(status=202)
        return Response(status=403)


class UserListView(APIView):
    def get(self, request):
        serializer = UsersSerializer(User.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        user = UsersSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response(status=201)
        return Response(status=400)


class UserView(APIView):
    def get(self, request, pk):
        obj = User.objects.filter(id=pk).first()
        if obj is None:
            return Response(status=404)
        return Response(UsersSerializer(obj).data)

    def put(self, request, pk):
        obj = User.objects.filter(id=pk).first()
        if obj is None:
            return Response(status=404)
        if obj != request.user and not request.user.is_staff:
            return Response(status=403)
        updated = UsersSerializer(obj, data=request.data, partial=True)
        if updated.is_valid():
            updated.save()
            return Response(status=202)
        return Response(status=400)

    def delete(self, request, pk):
        obj = User.objects.filter(id=pk).first()
        if obj is None:
            return Response(status=404)
        if obj != request.user and not request.user.is_staff:
            return Response(status=403)
        obj.delete()
        return Response(status=202)
