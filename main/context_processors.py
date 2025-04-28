from django.conf import settings

def main_settings(request):
    return {
        'SITE_TITLE': settings.SITE_TITLE
    }