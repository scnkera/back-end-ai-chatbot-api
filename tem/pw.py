from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'created_at']
        pw_hash = {
            'password': {'write_only': True}  # Ensure password is write-only
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)


    # def create(self, validated_data):
    #     validated_data['password'] = make_password(validated_data['password'])
    #     return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     if 'password' in validated_data:
    #         validated_data['password'] = make_password(validated_data['password'])
    #     return super().update(instance, validated_data)

# old user get/delete
# @api_view(['GET', 'DELETE'])
# def single_user(request, user_id):
#     try:
#         user = User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         raise Http404("User not found")

#     if request.method == 'GET':
#         serializer = UserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     elif request.method == 'DELETE':
#         user.delete()
#         return Response({'message': 'User deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

# first 4

@receiver(post_save, sender=User)
def assign_default_characters(sender, instance, created, **kwargs):
    if created:
        default_characters = Character.objects.all()[:4]  # Assign first 4 characters
        instance.characters.set(default_characters)

# get default options

# option 1 

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

# option 2

def get_default_conversation():
    system_user = User.objects.filter(username="system_user").first()
    neutral_character = Character.objects.filter(name="Neutral Character").first()
    
    if system_user and neutral_character:
        return Conversation.objects.filter(user=system_user, character=neutral_character).first()
    
    return None  # Fallback if data is missing

def get_default_training_message():
    neutral_character = Character.objects.filter(name="Neutral Character").first()
    
    if neutral_character:
        return TrainingMessage.objects.filter(character=neutral_character, user_input="PLACEHOLDER", response="PLACEHOLDER").first()
    
    return None  

