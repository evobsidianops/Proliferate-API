from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions

from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from knox.models import AuthToken

from .models import CustomUser
from .serializers import CustomUserSerializer, UserInfoSerializer

class CreateUser(APIView):
    """Create a new Custom user"""
    serializer_class = CustomUserSerializer

    def post(self, request, format=None):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            user = authenticate(request=request, email=serializer.validated_data['email'], 
                                password=serializer.validated_data['password'])
            
            logged_user = login(request, user)
            instance, token = AuthToken.objects.create(user)
        
            return Response({
                "data": serializer.data,
                "token": token,
                }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CreateUserInfo(APIView):
    """Create Info for specific Custom user"""
    serializer_class = UserInfoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
       print(request.user)
       try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
       except:
            return Response(serializer.errors, status=status.HTTP_201_CREATED)

class LoginView(KnoxLoginView):
    """Login view for authentication"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
         
        instance, token = AuthToken.objects.create(user)
        return Response({
            'token': token
        }, status=status.HTTP_200_OK)