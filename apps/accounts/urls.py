from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.CustomerRegistrationView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        success_url='/accounts/password-change-done/'), 
        name='password_change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'), 
        name='password_change_done'),
]

