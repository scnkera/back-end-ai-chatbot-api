from django.contrib import admin
from .models import User, Character, TrainingMessage, BotResponse

# admin.site.register(User)
# admin.site.register(Character)
# admin.site.register(TrainingMessage)
# admin.site.register(BotResponse)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'created_at')
    search_fields = ('username',)
    ordering = ('-created_at',)

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(TrainingMessage)
class TrainingMessageAdmin(admin.ModelAdmin):
    list_display = ('character', 'message', 'created_at')
    search_fields = ('message',)
    list_filter = ('character', 'created_at')
    ordering = ('-created_at',)

@admin.register(BotResponse)
class BotResponseAdmin(admin.ModelAdmin):
    list_display = ('character', 'user_input', 'response', 'created_at')
    search_fields = ('user_input', 'response')
    list_filter = ('character', 'created_at')
    ordering = ('-created_at',)