from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'created_at']
        pw_hash = {
            'password': {'write_only': True}  # Ensure password is write-only
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)


    # def create(self, validated_data):
    #     validated_data['password'] = make_password(validated_data['password'])
    #     return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     if 'password' in validated_data:
    #         validated_data['password'] = make_password(validated_data['password'])
    #     return super().update(instance, validated_data)