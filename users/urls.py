from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileUpdateView,
    UserRefreshTokenView,
    UserDeleteView,
    UserProfileView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('update_profile/', UserProfileUpdateView.as_view(), name='update_profile'),
    path('refresh_token/', UserRefreshTokenView.as_view(), name='refresh_token'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('delete/', UserDeleteView.as_view(), name='delete'),
]