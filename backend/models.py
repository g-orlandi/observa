import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError

from django.contrib.auth.models import Group

class MonitoredEntity(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=256, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="%(class)ss"
    )
    group = models.ForeignKey(
        Group,
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="%(class)ss"
    )
    logo = models.ImageField(upload_to='entity_pictures/', blank=True, null=True)

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        if not self.user and not self.group:
            raise ValidationError("An entity must be linked to at least a user or a group.")
        
    def save(self, *args, **kwargs):
        self.full_clean()  # chiama clean() + validatori dei campi
        super().save(*args, **kwargs)


class Server(MonitoredEntity):
    domain = models.CharField(
        max_length=253,
        validators=[RegexValidator(
            regex=r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$',
            message="Insert a valid domain"
        )]
    )
    port = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
        default=9100
    )

    def __str__(self):
        return f"{self.name} ({self.domain}:{self.port})"


class Endpoint(MonitoredEntity):
    url = models.URLField()
    check_keyword = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.url})"

class PromQuery(models.Model):

    class TargetSystem(models.TextChoices):
        PROMETHEUS = "prometheus", "Prometheus"
        UPTIME = "uptime", "Uptime Kuma"
        RESTIC = "restic", "Restic"


    title = models.CharField(max_length=50, help_text="Titolo descrittivo della query")
    code = models.SlugField(unique=True, help_text="Codice univoco senza spazi (es. 'cpu_usage')")
    expression = models.TextField(help_text="Espressione PromQL da eseguire")
    target_system = models.CharField(
        max_length=20,
        choices=TargetSystem.choices,
        default=TargetSystem.PROMETHEUS
    )

    def __str__(self):
        return f"{self.title} ({self.code})"
