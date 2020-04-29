from apps.users.models import UserOnline
from django.utils import timezone


class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        self.activate_user(request)
        return response

    def activate_user(self, request):
        current_user = request.user
        if current_user.is_authenticated:
            UserOnline.objects.update_or_create(user=current_user, defaults=dict(last_seen=timezone.now()))
