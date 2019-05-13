from django.urls import path
from django.contrib.auth import views as auth_views
from common import views
urlpatterns = [

    path('register/', views.RegisterView.as_view(), name='register'),
    path('update/<int:pk>/', views.UpdateProfile.as_view(), name='update'),
    path('info/<int:pk>/', views.UserProfileInfo.as_view(), name='user_info'),
    path('feedback/<int:pk>/', views.FeedBack.as_view(), name='feedback'),

    ]