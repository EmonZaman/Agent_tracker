import pytz

from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # TODO: get timezone from user
        user_agent: str = request.META.get('HTTP_USER_AGENT', '')
        tzname = request.session.get('django_timezone', 'Asia/Dhaka')
        if tzname and user_agent.find('okhttp') == -1:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
