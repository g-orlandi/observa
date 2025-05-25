import uuid
from datetime import datetime, timedelta, date

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q

from backend.models import Server, Endpoint
from main import settings

# Create your models here.
class User(AbstractUser):

    class Plan(models.IntegerChoices):
        FREE = 0, ('Free')
        PRO = 1, ('Pro')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    active_server = models.ForeignKey(
        Server,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='active_user'
    )
    active_backup_server = models.ForeignKey(
        Server,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='active_user_backup'
    )
    active_endpoint = models.ForeignKey(
        Endpoint,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='active_user'
    )
    filter_date_from = models.DateField('From', null=True, blank=True)
    filter_date_to = models.DateField('To', null=True, blank=True)

    plan = models.PositiveIntegerField(('Plan'), null=False, blank=False, choices=Plan.choices, default=0)

    REQUIRED_FIELDS = ['email'] # Used when creating superuser

    def __str__(self):
        text = self.get_full_name()
        if len(text) <= 0:
            text = self.username
        return text
    
    def get_active_date_filters(self):
        if self.filter_date_to is not None:
            date_to = self.filter_date_to
        else:
            date_to = date.today()
        if self.filter_date_from is not None:
            date_from = self.filter_date_from
        else:
            date_from = date_to - timedelta(days=2)
        return {
            'date_from': date_from,
            'date_to': date_to,
        }
    
    def set_active_date_filters(self, start_date, end_date):
        DATE_FORMAT = "%Y-%m-%d"
        start_date = datetime.strptime(start_date, DATE_FORMAT)
        end_date = datetime.strptime(end_date, DATE_FORMAT)

        if start_date > end_date:
            raise Exception("Start date cannot be after the end date.")
        else:
            self.filter_date_from = start_date
            self.filter_date_to = end_date
            self.save()

    def get_accessible_servers(self):
        # Remember: Django default is AND
        return Server.objects.filter(
            Q(user=self) | Q(group__in=self.groups.all())
        ).filter(is_backup=False).distinct()

    
    def get_accessible_servers_string(self):
        servers = self.get_accessible_servers()
        return "|".join(f"{s.domain}:{s.port}" for s in servers)

    def get_accessible_endpoints(self):
        # Remember: Django default is AND
        return Endpoint.objects.filter(
            Q(user=self) | Q(group__in=self.groups.all())
        ).distinct()

    def get_accessible_endpoints_string(self):
        endpoints = self.get_accessible_endpoints()
        return "|".join(f"{e.url}" for e in endpoints)

    def out_of_endpoints(self):
        if self.plan == User.Plan.FREE:
            n = Endpoint.objects.filter(user=self).count()
            if n >= settings.MAX_ENDPOINTS_FREE:
                return True
        return False
    
    def get_accessible_backup_servers(self):
        # Remember: Django default is AND
        return Server.objects.filter(
            Q(user=self) | Q(group__in=self.groups.all())
        ).filter(is_backup=True).distinct()

    def get_accessible_servers_string(self):
        servers = self.get_accessible_backup_servers()
        return "|".join(f"{s.domain}:{s.port}" for s in servers)

    @property
    def is_pro(self):
        return self.plan == User.Plan.PRO
    # def get_all_entities(self):
    #     servers = self.get_accessible_servers()
    #     endpoints = self.get_accessible_endpoints()
    #     combined = list(self.get_accessible_servers()) + list(self.get_accessible_endpoints())
    #     return combined