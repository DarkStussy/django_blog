from django.urls import path
from .views import login_user, register, profile, activate

app_name = 'accounts'

urlpatterns = [
    path('log-in/', login_user, name='login-user'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activate, name='activate'),
]
