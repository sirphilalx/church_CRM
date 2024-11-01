from rest_framework import serializers
from .models import CustomUser
from rest_framework import permissions

class IsAdminOrSecretary(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'secretary']

class IsZonalHead(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'zonal_head'

    def has_object_permission(self, request, view, obj):
        return obj.zone == request.user.zone 

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'firstname', 'middlename', 'lastname', 'email', 
                  'address', 'zone', 'date_of_birth', 'password', 
                  'phone_number1', 'phone_number2', 'role']
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def validate(self, data):
        # You can add any extra validation here
        if 'phone_number1' not in data and 'phone_number2' not in data:
            raise serializers.ValidationError("At least one phone number is required.")
        return data

class UserSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'firstname', 'lastname', 'date_of_birth', 'email', 'role', 'address', 'zone', 'phone_number1', 'phone_number2']