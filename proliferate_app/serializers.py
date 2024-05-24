from rest_framework import serializers
from .models import CustomUser, UserInfo

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def create(self, validated_data):
        """
        Create new custom user
        """
        return CustomUser.objects.create_user(**validated_data)
    
class UserInfoSerializer(serializers.ModelSerializer):
    """Create UserInfo for specific Custom User"""
    class Meta:
        model = UserInfo
        fields = '__all__'