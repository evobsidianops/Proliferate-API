from django.urls import path
from knox.views import LogoutView

from .views import CreateUser, CreateUserInfo, LoginView

urlpatterns = [
    path('api/register_user/', CreateUser.as_view(), name='user'),
    path('api/create_user_info/', CreateUserInfo.as_view(), name='detail')
]

urlpatterns += [
     path('auth/login/', LoginView.as_view(), name='knox_login'),
     path('auth/logout/', LogoutView.as_view(), name='knox_logout')
]