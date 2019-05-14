from django.urls import path

from .views.common_views import (MobileHomePageView,MobileRegisterView, MobileLoginView,
                                 MobileUserInfo)


urlpatterns = [
    path('', MobileHomePageView.as_view(), name='home'),
    path('register/', MobileRegisterView.as_view(), name='register'),
    path('login/', MobileLoginView.as_view(), name='login'),
    path('user/<int:pk>/', MobileUserInfo.as_view(), name='user_info'),

]
