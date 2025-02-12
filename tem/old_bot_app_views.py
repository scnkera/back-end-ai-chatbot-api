from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import User, Character, BotResponse, TrainingMessage, Conversation, get_default_training_message
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
        return JsonResponse({"training_messages": data})
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
# @api_view(['GET', 'POST'])
# def conversations(request):
#     if request.method == 'GET':
#         conversations = Conversation.objects.all()
#         serializer = ConversationSerializer(conversations, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     elif request.method == 'POST':
#         serializer = ConversationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'DELETE'])
# def single_conversation(request, conversation_id):
#     conversation = get_object_or_404(Conversation, id=conversation_id)

#     if request.method == 'GET':
#         serializer = ConversationSerializer(conversation)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     elif request.method == 'DELETE':
#         conversation.delete()
#         return Response({'message': 'Conversation deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

#     def get_conversation_history(user, character):
#     try:
#         conversation = Conversation.objects.get(user=user, character=character)
#         responses = BotResponse.objects.filter(conversation=conversation).order_by('created_at')
        
#         history = [
#             {"user_input": resp.user_input, "bot_response": resp.response, "timestamp": resp.created_at}
#             for resp in responses
#         ]
        
#         return history
#     except Conversation.DoesNotExist:
#         return None 


# @api_view(['POST'])
# def save_bot_response(request, user_id, character_id):
#     """Save a new user input and bot response into the conversation history"""
#     user_input = request.data.get("user_input")
#     bot_response = request.data.get("bot_response")

#     if not user_input or not bot_response:
#         return Response({"error": "Both user_input and bot_response are required."}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         user = User.objects.get(id=user_id)
#         character = Character.objects.get(id=character_id)
#     except User.DoesNotExist:
#         return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
#     except Character.DoesNotExist:
#         return Response({"error": "Character not found."}, status=status.HTTP_404_NOT_FOUND)

#     # Check if a conversation exists between the user and character, or create one
#     conversation, created = Conversation.objects.get_or_create(user=user, character=character)

#     training_message = TrainingMessage.objects.filter(
#         character=character, user_input=user_input
#     ).first()
    
#     if training_message is None:
#         training_message = get_default_training_message()  # or simply None

#     # # Try to find a matching TrainingMessage (optional)
#     # training_message = TrainingMessage.objects.filter(character=character, user_input=user_input).first()
#     # if not training_message:
#     #     training_message = None  # Or set a default if necessary

#     # Create and save the BotResponse entry
#     bot_response_obj = BotResponse.objects.create(
#         character=character,
#         training_message=training_message,  # Could be None
#         user_input=user_input,
#         response=bot_response,
#         conversation=conversation
#     )

#     return Response(BotResponseSerializer(bot_response_obj).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def save_bot_response(request, user_id, character_id):
    """Save a new user input and bot response into the conversation history"""
    user_input = request.data.get("user_input")
    bot_response = request.data.get("bot_response")

    if not user_input or not bot_response:
        return Response({"error": "Both user_input and bot_response are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(id=user_id)
        character = Character.objects.get(id=character_id)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Character.DoesNotExist:
        return Response({"error": "Character not found."}, status=status.HTTP_404_NOT_FOUND)

    # Check if a conversation exists between the user and character, or create one
    conversation, created = Conversation.objects.get_or_create(user=user, character=character)

    # Retrieve the TrainingMessage based on user_input and character
    training_message = TrainingMessage.objects.filter(
        character=character, user_input=user_input
    ).first()
    
    # If no matching training_message, use default or None
    if not training_message:
        # Use a function to get default message or just set to None
        training_message = get_default_training_message()  # You can modify this function to return a default message or None.

    # Create and save the BotResponse entry
    bot_response_obj = BotResponse.objects.create(
        character=character,
        training_message=training_message,  
        user_input=user_input,
        response=bot_response,
        conversation=conversation
    )

    return Response(BotResponseSerializer(bot_response_obj).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def conversation_history(request, user_id, character_id):
    user = get_object_or_404(User, id=user_id)
    character = get_object_or_404(Character, id=character_id)

    # Get the conversation
    conversation = Conversation.objects.filter(user=user, character=character).first()
    if not conversation:
        return Response({"message": "No conversation history found."}, status=status.HTTP_200_OK)

    # Get all bot responses tied to this conversation
    bot_responses = BotResponse.objects.filter(conversation=conversation).order_by("created_at")
    
    serializer = BotResponseSerializer(bot_responses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




# URLS

    # path('conversations/', views.conversations, name='conversations-list'),
    # path('conversations/<int:conversation_id>/', views.single_conversation, name='conversations-detail'),

# OLD MODELS

    # training_message = models.ForeignKey(
    #     TrainingMessage, on_delete=models.CASCADE, default=get_default_training_message
    # )  # Prevents null values