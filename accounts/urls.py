from django.urls import path
from .views import login_user, register, profile

app_name = 'accounts'

urlpatterns = [
    path('log-in/', login_user, name='login-user'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
]
