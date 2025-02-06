from django.contrib import admin
from .models import User, Character, TrainingMessage, BotResponse, Conversation

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'created_at')  # Display username and created_at
    search_fields = ('username',)  # Allow searching by username
    ordering = ('-created_at',)  # Sort users by newest first
    filter_horizontal = ('characters',)  # Use a better UI for ManyToManyField

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(TrainingMessage)
class TrainingMessageAdmin(admin.ModelAdmin):
    list_display = ('character', 'user_input', 'response', 'created_at')
    search_fields = ('user_input', 'response')
    list_filter = ('character', 'created_at')
    ordering = ('-created_at',)

@admin.register(BotResponse)
class BotResponseAdmin(admin.ModelAdmin):
    list_display = ('character', 'user_input', 'response', 'conversation', 'created_at')
    search_fields = ('user_input', 'response')
    list_filter = ('character', 'conversation', 'created_at')
    ordering = ('-created_at',)

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('user', 'character', 'started_at')
    search_fields = ('user__username', 'character__name')  # Search by user and character
    list_filter = ('character', 'started_at')
    ordering = ('-started_at',)
