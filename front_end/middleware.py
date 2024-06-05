from django.utils import timezone
from datetime import timedelta
from .models import PageVisit, Statistics

class PageVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and request.user.username != 'admin' and request.path != '/favicon.ico':
            statistics = Statistics.objects.first()
            time_remaining = statistics.total_time if statistics else None
            PageVisit.objects.create(user=request.user, page=request.path, time_remaining=time_remaining)

        return response
