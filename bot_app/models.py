from django.db import models
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password

class User(models.Model):
    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    characters = models.ManyToManyField('Character', related_name='users')
    created_at = models.DateTimeField(default=now)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.username


class Character(models.Model):
    name = models.CharField(max_length=50)
    title = models.TextField()
    biography = models.TextField()
    created_at = models.DateTimeField(default=now)

    class Meta:
        db_table = "character"

    def __str__(self):
        return self.name


class TrainingMessage(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="training_messages")
    user_input = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=now)

    class Meta:
        db_table = "training_message"

    def __str__(self):
        return f"TrainingMessage for {self.character.name}"


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conversation"

    def __str__(self):
        return f"Conversation between {self.user.username} and {self.character.name}"


def get_default_conversation():
    try:
        system_user = User.objects.get(username="system_user")
        neutral_character = Character.objects.get(name="Neutral Character")
        return Conversation.objects.get(user=system_user, character=neutral_character)
    except (User.DoesNotExist, Character.DoesNotExist, Conversation.DoesNotExist):
        return None


def get_default_training_message():
    try:
        neutral_character = Character.objects.get(name="Neutral Character")
        return TrainingMessage.objects.get(character=neutral_character, user_input="PLACEHOLDER", response="PLACEHOLDER")
    except (Character.DoesNotExist, TrainingMessage.DoesNotExist):
        return None


class BotResponse(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    training_message = models.ForeignKey(
        TrainingMessage, on_delete=models.CASCADE, default=get_default_training_message
    )  # Prevents null values
    user_input = models.TextField(blank=True, null=True)
    response = models.TextField()
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE, related_name='responses', default=get_default_conversation)
    created_at = models.DateTimeField(default=now)

    class Meta:
        db_table = "bot_response"

    def __str__(self):
        return f"The response to '{self.user_input}' was '{self.response}'"
