from django.apps import AppConfig

from django.contrib.auth import get_user_model


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # Function ready is called one time, when Django is loading the application
    def ready(self):
        # We obtain dinamically the user model of our application. In this case, that's our customized user model.
        User = get_user_model() 

        # We force this variable in order to let Django think that our customized user model is part of the original auth app.
        # This make Django show the user model in the right section of the admin and not in another one.
        User._meta.app_label = 'auth' 