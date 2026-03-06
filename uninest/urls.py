"""
URL configuration for uninest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # 建议这样导入 settings
from django.conf.urls.static import static # 必须导入 static 函数
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('properties.urls')),
    

]
# 在列表外部添加 static 配置
if settings.DEBUG: # 建议只在开发模式下开启
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

