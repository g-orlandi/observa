import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError

from django.contrib.auth.models import Group

class Server(models.Model):
    id = models.UUIDField('id', default=uuid.uuid4, primary_key=True, unique=True,
        null=False, blank=False, editable=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=256, null=False, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='servers'
    )
    group = models.ForeignKey(
        Group,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='servers'
    )
    logo = models.ImageField(upload_to='server_pictures/', blank=True, null=True)
    domain = models.CharField(
        max_length=253,
        validators=[RegexValidator(regex=r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$',message="Insert a valid domain")],
        null=False,
        blank=False
    )
    port = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
        default=9100
    )
    
    def __str__(self):
        return f"{self.name} ({self.domain}:{self.port})"
    
    def clean(self):
        super().clean()
        if not self.user and not self.group:
            raise ValidationError("A server must be linked to at least a user or a group.")

    def save(self, *args, **kwargs):
        self.full_clean()  # chiama clean() prima del salvataggio
        super().save(*args, **kwargs)
    
class PromQuery(models.Model):
    
    class QType(models.IntegerChoices):
        SINGLE = 0, ('Single')
        RANGE = 1, ('Range')

    title = models.CharField(max_length=50, help_text="Titolo descrittivo della query")
    code = models.SlugField(unique=True, help_text="Codice univoco senza spazi (es. 'cpu_usage')")
    expression = models.TextField(help_text="Espressione PromQL da eseguire")
    qtype = models.PositiveIntegerField(('QType'), null=False, blank=False, choices=QType.choices, default=0)

    def __str__(self):
        return f"{self.title} ({self.code})"
