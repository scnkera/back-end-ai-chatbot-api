from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from .models import User, Character, TrainingMessage, Conversation
import os
import json

DEFAULT_USERNAME = "system_user"
DEFAULT_CHARACTER_NAME = "Neutral Character"
# TRAINED_MSG_DIR = os.path.join(os.path.dirname(__file__), "trained_msg")
TRAINED_MSG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "trained_msg"))

# Helper Functions

def load_character_metadata():
    characters_file = os.path.join(TRAINED_MSG_DIR, "characters.json")
    if not os.path.exists(characters_file):
        return [] 
    with open(characters_file, "r", encoding="utf-8") as f:
        return json.load(f)

def load_character_training_messages(character_name):
    filename = f"{character_name.lower().replace(' ', '_')}.json"
    file_path = os.path.join(TRAINED_MSG_DIR, filename)

    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("training_messages", []) 

@receiver(post_migrate)
def create_default_data(sender, **kwargs):
    if sender.name != "bot_app":
        return 

    # creates system user
    system_user, _ = User.objects.get_or_create(
        username=DEFAULT_USERNAME,
        defaults={"password": make_password("default_password")}
    )

    # creates neutral character
    neutral_character, _ = Character.objects.get_or_create(
        name=DEFAULT_CHARACTER_NAME,
        defaults={"title": "Default title", "biography": "Default character for system messages."}
    )

    # creates celebrity characters and their training messages
    characters = load_character_metadata()

    for character_data in characters:
        character, _ = Character.objects.get_or_create(
            name=character_data["name"],
            defaults={
                "biography": character_data.get("biography", ""),
                "title": character_data.get("title", "")
            }
        )

        training_messages = load_character_training_messages(character.name)
        for message in training_messages:
            TrainingMessage.objects.get_or_create(
                character=character,
                user_input=message.get("user_input", ""),
                response=message.get("response", "")
            )

    # create a default conversation for the system user
    Conversation.objects.get_or_create(user=system_user, character=neutral_character)
