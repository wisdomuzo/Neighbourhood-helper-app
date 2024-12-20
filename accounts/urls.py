
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import password_reset_request_view

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.view_profile, name='profile_view'),
    path('profile/edit/', views.create_or_edit_profile, name='profile_edit'),
    # Password reset URLs
    path('password_reset/', password_reset_request_view, name='password_reset'),  # Custom request view
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Users' rating url 
    path('rate_user/<int:user_id>/', views.rate_user, name='rate_user'),

]