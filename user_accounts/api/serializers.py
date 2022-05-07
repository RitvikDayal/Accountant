"""
Contains Serializers for the User Accounts API for JWT Authentication.
"""


from user_accounts.models import User

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework import serializers

from utils.utilities import get_tokens_for_user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for 1FA login authentication.
    """

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    user_name = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):

        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'User with given email and password does not exists.',
            )
        try:
            tokens = get_tokens_for_user(user)
            update_last_login(None, user)

        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists',
            )
        return {
            'user_name': user.get_full_name,
            'email': user.email,
            'access_token': tokens['access'],
            'refresh_token': tokens['refresh'],
        }
