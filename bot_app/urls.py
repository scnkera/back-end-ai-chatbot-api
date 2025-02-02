from django.urls import path
from . import views

urlpatterns = [

    #index
    path('', views.index, name='index'),

    # user
    path('users', views.users, name='users'),
    path('users/<int:user_id>', views.single_user, name='single_user'),

    # character
    path('characters', views.characters, name='characters'),
    path('characters/<int:character_id>', views.single_character, name='single_character'),

    # training_message
    path('training_messages', views.training_messages, name='training_messages'),
    path('training_messages/<int:message_id>', views.single_training_message, name='single_training_message'),

    # bot_response
    path('bot_responses', views.bot_responses, name='bot_responses'),
    path('bot_responses/<int:response_id>', views.single_bot_response, name='single_bot_response'),
]