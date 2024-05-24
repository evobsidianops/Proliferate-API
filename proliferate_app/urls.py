from django.urls import path
from knox import views as knox_views

from .views import CreateUser, CreateUserInfo, LoginView

urlpatterns = [
    path('user/', CreateUser.as_view(), name='user'),
    path('detail/', CreateUserInfo.as_view(), name='detail')
]

urlpatterns += [
     path('login/', LoginView.as_view(), name='knox_login'),
     path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
     path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),]