from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.models import User

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')  # 显示用户名、密码和身份
    search_fields = ('user__username',)  # 添加搜索功能

    # 自定义显示用户名和密码字段
    def username(self, obj):
        return obj.user.username
    username.short_description = '用户名'

    def password(self, obj):
        return obj.user.password
    password.short_description = '密码'


# 注册模型
admin.site.register(CustomUser, CustomUserAdmin)
