from django.http import HttpResponseForbidden
from functools import wraps

def require_pro_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_pro:
            return HttpResponseForbidden("Reserved for PRO users.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
