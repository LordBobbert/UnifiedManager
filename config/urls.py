# File: backend/config/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Authentication and Registration
    path('api/auth/', include('dj_rest_auth.urls')),  # Login, Logout, Password Reset
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  # Registration
    path('api/auth/social/', include('allauth.socialaccount.urls')),  # Social Authentication

    # Users App
    path('api/users/', include('users.urls')),  # Endpoints for Clients and Trainers

    # Quickbooks
    path('api/quickbooks/', include('quickbooks.urls')),

]
