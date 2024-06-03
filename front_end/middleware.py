from django.utils import timezone
from datetime import timedelta
from .models import PageVisit

class PageVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and request.user.username != 'admin':
            timestamp = timezone.now() + timedelta(hours=1)
            PageVisit.objects.create(user=request.user, page=request.path, timestamp=timestamp)

        return response