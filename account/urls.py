from django.urls import path

from account.views import (
    ChangePasswordView,
    LoginView,
    LogoutView,
    ProfileEditModalView,
    ProfileView,
    RegisterView,
    SettingsView,
)

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/editar/', ProfileEditModalView.as_view(), name='profile_edit'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]
