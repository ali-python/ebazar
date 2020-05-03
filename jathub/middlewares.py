import re
import logging

from django.urls import resolve, reverse
from django.http import HttpResponseRedirect, Http404

from django.conf import settings


class MobileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",
                                     re.IGNORECASE)
        if settings.MOBILE_ENABLED and not hasattr(request, 'is_mobile'):
            request.is_mobile = False
            request.mobile_type = ''

        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            request.is_mobile = True

        if settings.MOBILE_ENABLED and \
                hasattr(request, 'is_mobile') and request.is_mobile:
            request.urlconf = 'jathub.mobile_urls'

        response = self.get_response(request)
        return response


class CommonMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if not hasattr(request, 'is_mobile'):
            request.is_mobile = False
            request.mobile_type = ''
        if request.user.is_authenticated and not request.user.is_active and not request.path == reverse(
                'logout'):
            return HttpResponseRedirect(reverse('logout'))
        if 'windows' in request.META.get('HTTP_USER_AGENT', '').lower():
            request.is_windows = True
        else:
            request.is_windows = False

        if '/api/' in request.path:
            request.is_api = True
        else:
            request.is_api = False

        if request.META.get('HTTP_COUNTRY', ''):
            request.session['country'] = request.META['HTTP_COUNTRY']
            request.country = request.META['HTTP_COUNTRY']
        elif not hasattr(request, 'country'):
            request.country = 'AE'

        response = self.get_response(request)

        return response
