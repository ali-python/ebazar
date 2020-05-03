from django.conf import settings


def settings_context(request):
    context = {
        'LOCAL_ENV': settings.LOCAL_ENV
    }
    return context