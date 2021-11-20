from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from .managers import UserManager
from django.core import validators


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(validators=[validators.validate_email], unique=True)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=30)
    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)
    is_active = models.BooleanField('active', default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Post(models.Model):
    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    publication_time = models.DateTimeField(verbose_name='Время публикации', auto_now=True)


class Comment(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    body = models.TextField()
    publication_time = models.DateTimeField(verbose_name='Время публикации', auto_now=True)
