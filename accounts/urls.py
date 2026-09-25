from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('password/change/', views.password_change_view, name='password_change'),
    path(
        'password/reset/',
        PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            email_template_name='accounts/password_reset_email.html',
            subject_template_name='accounts/password_reset_subject.txt',
            success_url='/accounts/password/reset/done/',
        ),
        name='password_reset',
    ),
    path(
        'password/reset/done/',
        PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'password/reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html',
            success_url='/accounts/password/reset/complete/',
        ),
        name='password_reset_confirm',
    ),
    path(
        'password/reset/complete/',
        PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
]
