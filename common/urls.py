from django.urls import path
from django.contrib.auth import views as auth_views
from common import views
urlpatterns = [

    path('register/', views.RegisterView.as_view(), name='register'),

    ]