from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Character, BotResponse, TrainingMessage, Conversation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': False, 'allow_null': True},
            'last_name': {'required': False, 'allow_null': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['id', 'name', 'title', 'biography', 'created_at']

class TrainingMessageSerializer(serializers.ModelSerializer):
    character = CharacterSerializer(read_only=True)

    class Meta:
        model = TrainingMessage
        fields = ['id', 'character', 'user_input', 'response', 'created_at']

class BotResponseSerializer(serializers.ModelSerializer):
    character = CharacterSerializer(read_only=True) 
    training_message = TrainingMessageSerializer(read_only=True) 
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all()) 

    class Meta:
        model = BotResponse
        fields = ['id', 'character', 'training_message', 'user_input', 'response', 'conversation', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    character = CharacterSerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'user', 'character', 'started_at']
