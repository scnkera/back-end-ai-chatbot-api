from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import User, Character, BotResponse, TrainingMessage
from .serializers import UserSerializer, CharacterSerializer, BotResponseSerializer, TrainingMessageSerializer, ConversationSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import Http404

def index(request):
    return HttpResponse("This is my first URL")

# users
@api_view(['GET', 'POST'])
def users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User profile created successfully!', 'user': serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
def single_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        user.delete()
        return Response({'message': 'User deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User profile updated successfully!', 'user': serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# characters
@api_view(['GET', 'POST'])
def characters(request):
    if request.method == 'GET':
        characters = Character.objects.all()
        serializer = CharacterSerializer(characters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CharacterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def single_character(request, character_id):
    character = get_object_or_404(Character, id=character_id)

    if request.method == 'GET':
        serializer = CharacterSerializer(character)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        character.delete()
        return Response({'message': 'Character deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# training messages
@api_view(['GET', 'POST'])
def training_messages(request):
    if request.method == 'GET':
        messages = TrainingMessage.objects.all()
        serializer = TrainingMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = TrainingMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def single_training_message(request, message_id):
    message = get_object_or_404(TrainingMessage, id=message_id)

    if request.method == 'GET':
        serializer = TrainingMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        message.delete()
        return Response({'message': 'Training message deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

def get_character_training_messages(request, character_name):
    try:
        character = Character.objects.get(name=character_name) 
        messages = character.training_messages.all()
        data = [{"user_input": msg.user_input, "response": msg.response} for msg in messages]
        return JsonResponse({"messages": data})
    except Character.DoesNotExist:
        return JsonResponse({"error": "Character not found"}, status=404)


# bot responses
@api_view(['GET', 'POST'])
def bot_responses(request):
    if request.method == 'GET':
        responses = BotResponse.objects.all()
        serializer = BotResponseSerializer(responses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = BotResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def single_bot_response(request, response_id):
    response = get_object_or_404(BotResponse, id=response_id)

    if request.method == 'GET':
        serializer = BotResponseSerializer(response)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        response.delete()
        return Response({'message': 'Bot response deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# conversations
@api_view(['GET', 'POST'])
def conversations(request):
    if request.method == 'GET':
        conversations = Conversation.objects.all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def single_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    if request.method == 'GET':
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        conversation.delete()
        return Response({'message': 'Conversation deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
