from django.apps import AppConfig

class BotappConfig(AppConfig):
   default_auto_field = 'django.db.models.BigAutoField'
   name = 'bot_app'


   def ready(self):
      import app_bot.signals



