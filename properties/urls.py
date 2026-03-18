from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('home/', views.home, name='home'),
    path("register/", views.register, name="register"),
    path('login/', LoginView.as_view(template_name="login.html", next_page='home'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/user/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/agency/', views.agency_dashboard, name='agency_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/add/', views.post_property, name='post_property'),
    
    path('my-collection/', views.my_collection, name='my_collection'),
    path('user-info/', views.user_info, name='user_info'),
    path('agency-info/', views.agency_info, name='agency_info'),
    path('profile/edit/', views.edit_user_profile, name='edit_user_profile'),
    path('profile/agency/edit/', views.edit_agency_profile, name='edit_agency_profile'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password/password_reset_form.html'), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),

    path('property/<int:pk>/like/', views.toggle_like, name='toggle_like'),

    path('my-likes/', views.my_likes, name='my_likes'),
    
    path('property/<int:pk>/collect/', views.toggle_collection, name='toggle_collection'),
    
    path('agency/<int:user_id>/', views.agency_info, name = 'agency_info')
]
