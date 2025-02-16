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
    path("training_messages/<str:character_name>/", views.get_character_training_messages, name='get_character_training_messages'),

    # Bot Response
    path('bot_responses/', views.bot_responses, name='bot_responses-list'),
    path('bot_responses/<int:response_id>/', views.single_bot_response, name='bot_responses-detail'),

    # Conversation

    path('conversation/<int:user_id>/<int:character_id>/save/', views.save_bot_response, name='save_bot_response'),
    path('conversation/<int:user_id>/<int:character_id>/', views.conversation_history, name='conversation_history'),
]
