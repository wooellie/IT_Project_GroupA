from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views # 引入官方视图
urlpatterns = [
    # --- 核心页面 ---
    path('', views.home, name='home'),
    path("register/", views.register, name="register"),
    # 这里的 template_name 要确保路径正确。按你现在的结构 login.html 在 templates 根目录下，所以不用改
    path('login/', LoginView.as_view(template_name="login.html", next_page='home'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # --- 仪表盘与分发 (Dashboard) ---
    # 虽然登录跳首页，但导航栏通常需要一个“我的中心”按钮，这时 dashboard_redirect 就很有用
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/user/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/agency/', views.agency_dashboard, name='agency_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    # --- 房源相关功能 (M3 & M5) - 新增建议 ---
    # 房源详情页，使用主键 pk 来定位
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    # 中介发布房源
    path('property/add/', views.post_property, name='post_property'),
    
    # --- 收藏与个人信息 (M5 & Sitemap 子页面) - 新增建议 ---
    path('my-collection/', views.my_collection, name='my_collection'),
    path('user-info/', views.user_info, name='user_info'),
    path('agency-info/', views.agency_info, name='agency_info'),

    # 1. 发起重置请求页面
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password/password_reset_form.html'), name='password_reset'),
    
    # 2. 邮件已发送提示页
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    
    # 3. 用户点击邮件链接后的设置新密码页
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'), name='password_reset_confirm'),
    
    # 4. 重置成功页
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),

    # 点赞功能的 URL
    path('property/<int:pk>/like/', views.toggle_like, name='toggle_like'),

    # 我的点赞列表页
    path('my-likes/', views.my_likes, name='my_likes'),

    # 收藏功能的 URL
    path('my-collection/', views.my_collection, name='my_collection'),
    
    # 切换收藏状态的 URL
    path('property/<int:pk>/collect/', views.toggle_collection, name='toggle_collection'),
]