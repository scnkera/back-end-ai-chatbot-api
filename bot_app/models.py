from django.db import models
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password


class User(models.Model):
    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.username


class Character(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=5000)
    created_at = models.DateTimeField(default=now)

    class Meta:
        db_table = "character"

    def __str__(self):
        return self.name

class TrainingMessage(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="training_messages")
    message = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(default=now)

    class Meta:
        db_table = "training_message"

    def __str__(self):
        return f"TrainingMessage for {self.character.name}"

class BotResponse(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    training_message = models.ForeignKey(TrainingMessage, on_delete=models.SET_NULL, null=True, blank=True)
    user_input = models.CharField(max_length=50, blank=True, null=True)
    response = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=now)

    class Meta:
        db_table = "bot_response"

    def __str__(self):
        return f"The response to '{self.user_input}' was '{self.response}'"