from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import User, Property

admin.site.register(Property)

# 注册自定义 User 模型，使用系统内置的 UserAdmin 样式
admin.site.register(User, UserAdmin)