from django.conf import settings

def main_settings(request):
    return {
        'SITE_TITLE': settings.SITE_TITLE,
        'IS_USER_PRO': request.user.is_pro(),
    }