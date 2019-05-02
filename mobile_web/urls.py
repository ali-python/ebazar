from django.urls import path

from .views.common_views import MobileHomePageView

urlpatterns = [
    path('', MobileHomePageView.as_view(), name='home'),
]
