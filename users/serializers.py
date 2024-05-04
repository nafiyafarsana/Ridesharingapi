from rest_framework import serializers
from .models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','email','password']
        

    def validate(self, data):

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('username has already taken')
        
        if User.objects.filter(username=data['email']).exists():
            raise serializers.ValidationError('email has already taken')
        
        return data 
    
    def create(self,validated_data):
         user = User.objects.create(
             username = validated_data['username'],
             email = validated_data['email']
         )

         user.set_password(validated_data['password'])
         user.save()

         return user
    

    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if not User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Email does not exist')
        return data

    def get_jwt_token(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            return None 
        refresh = RefreshToken.for_user(user)
        return {
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        }