import datetime
from django.core.cache import cache
from Django_ECommerce import settings


class ActiveUserMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        current_user = request.user
        if request.user.is_authenticated:
            now = datetime.datetime.now()
            cache.set('seen_%s' % (current_user.username), now, settings.USER_LASTSEEN_TIMEOUT)


        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

