from rest_framework import serializers
from .models import User, Character, BotResponse, TrainingMessage

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['id', 'name', 'description', 'created_at']

class TrainingMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingMessage
        fields = ['id', 'character', 'message', 'created_at']

class BotResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotResponse
        fields = ['id', 'character', 'training_message', 'user_input', 'response', 'created_at']
