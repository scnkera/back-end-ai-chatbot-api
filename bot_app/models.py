from django.db import models
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password


class User(models.Model):
    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(default=now)


    def __str__(self):
        return self.username
