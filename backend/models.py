import uuid
from django.db import models
from django.conf import settings

class Server(models.Model):
    id = models.UUIDField('id', default=uuid.uuid4, primary_key=True, unique=True,
        null=False, blank=False, editable=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=256, null=False, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='server_pictures/', blank=True, null=True)

    def __str__(self):
        return self.name