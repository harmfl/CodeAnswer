from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,AbstractUser
from django.db import models
from django.contrib.auth.models import User

# class CustomUser(AbstractUser):
#     # 只保留账号和密码字段
#     username = models.CharField(max_length=150, unique=True)
#     password = models.CharField(max_length=128)
#     email = models.EmailField(unique=True, blank=True, null=True)
#
#     # 添加必要的字段
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#
#     USERNAME_FIELD = 'username'  # 设定账号为登录时使用的字段
#     REQUIRED_FIELDS = []  # 因为没有其他必填字段，留空即可
#
#     # objects = CustomUserManager()  # 设置自定义的Manager
#
#     def __str__(self):
#         return self.username

class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    # 其他字段定义
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"

    def re_id(self):
        return self.user.id
