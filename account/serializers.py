import re

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import AppUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    phone_number = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = AppUser
        fields = (
            'email', 'username', 'first_name', 'last_name', 'gender', 'phone_number', 'password', 'confirm_password')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_number': {'required': True}
        }

    def validate_phone_number(self, value):
        regex = '([+]?01[0125]\d{8})'
        phone = re.fullmatch(regex, value)
        if phone is None:
            raise serializers.ValidationError(
                {"phone": "Incorrect phone Number format 11 digits,it must start with 010,011,012, or 015."})
        return value

    def validate_username(self, value):
        regex = '([a-z][a-z0-9_.-]{1,22})'
        username = re.fullmatch(regex, value)
        if username is None:
            raise serializers.ValidationError({"username": "Incorrect UserName format must start with lowercase alpha "
                                                           "and only contains digits , . ,_ characters"})
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = AppUser.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username is None or password is None:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials.")
        return user
