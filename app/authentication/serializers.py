from rest_framework import serializers
from authentication.models import User

class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(min_length=8, write_only=True)
    
    class Meta:
        model=User
        fields = ('id', 'first_name', 'last_name', 'email', 'gender', 'age', 'weight', 'password')
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class LoginSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields = ('id', 'email', 'token', 'password')
        read_only_fields = ['token']
        
class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    class Meta:
        model=User
        fields = ('id', 'first_name', 'last_name', 'email', 'gender', 'age', 'weight', 'password')