from rest_framework import serializers

from authentication_app.models import AppUser


class UserSerializer(serializers.ModelSerializer):
    '''User Serializer Class for data serializing and deserializing'''

    class Meta:
        model = AppUser
        fields = ["first_name", "last_name", "email", "password"]

class SignInRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

class TokenField(serializers.Field):
    '''Custom class to create token field by converting token bytes to string'''
    
    def to_representation(self, data):
        return bytes.decode(data)

class SignInResponseSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=150)
    token = TokenField()

class SignUpResponseSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=150)
