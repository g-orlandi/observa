import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from backend.models import Server  # importa solo se già esiste

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    active_server = models.ForeignKey(
        Server,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='active_user'
    )

    def __str__(self):
        text = self.get_full_name()
        if len(text) <= 0:
            text = self.username
        return text