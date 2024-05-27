from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions

from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from knox.models import AuthToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import CustomUser
from .serializers import CustomUserSerializer, UserInfoSerializer

class CreateUser(APIView):
    """Create a new Custom user"""
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="User unique email"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="User unique email")
            }
        )
    )
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

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token must start with 'Token' before actual token. ex. Authorization: Token 2ggw45254", type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(type=openapi.TYPE_INTEGER, description=" User Foreign key"),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description="first name"),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description="last name"),
                'contact_number': openapi.Schema(type=openapi.TYPE_STRING, description="Contact number"),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, description="gender"),
                'age': openapi.Schema(type=openapi.TYPE_INTEGER, description="age"),
                'grade_or_year': openapi.Schema(type=openapi.TYPE_STRING, description="grade or year"),
                'current_location': openapi.Schema(type=openapi.TYPE_STRING, description="current location"),
                'subjects': openapi.Schema(type=openapi.TYPE_STRING, description="subjects"),
                'attendance': openapi.Schema(type=openapi.TYPE_STRING, description="attendance"),
                'availability': openapi.Schema(type=openapi.TYPE_STRING, description="availability"),
                'additional_preferences': openapi.Schema(type=openapi.TYPE_STRING, description="Additional preferences"),
                'communication_language': openapi.Schema(type=openapi.TYPE_STRING, description="Communication Language"),
                'short_term_goals': openapi.Schema(type=openapi.TYPE_STRING, description="Short term goals"),
                'long_term_goals': openapi.Schema(type=openapi.TYPE_STRING, description="Long term goals")
            },
            required=['user', 'first_name', 'last_name', 'contact_number', 'availability', 'communication_language']
        ),
        security=[{'Bearer': []}],
    )
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
    """Login view that generates a token for authentication and authorization"""
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="username is user unique email address"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="password")
            }
        )
    )
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
         
        instance, token = AuthToken.objects.create(user)
        return Response({
            'token': token
        }, status=status.HTTP_200_OK)