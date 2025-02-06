from django.urls import path
from . import views

urlpatterns = [
    # Index
    path('', views.index, name='index'),

    # User
    path('users/', views.users, name='users-list'),
    path('users/<int:user_id>/', views.single_user, name='users-detail'),

    # Character
    path('characters/', views.characters, name='characters-list'),
    path('characters/<int:character_id>/', views.single_character, name='characters-detail'),

    # Training Message
    path('training_messages/', views.training_messages, name='training_messages-list'),
    path('training_messages/<int:message_id>/', views.single_training_message, name='training_messages-detail'),

    # Bot Response
    path('bot_responses/', views.bot_responses, name='bot_responses-list'),
    path('bot_responses/<int:response_id>/', views.single_bot_response, name='bot_responses-detail'),

    # Conversation
    path('conversations/', views.conversations, name='conversations-list'),
    path('conversations/<int:conversation_id>/', views.single_conversation, name='conversations-detail'),
]
