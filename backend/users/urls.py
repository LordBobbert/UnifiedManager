# File: backend/users/urls.py

from django.urls import path
from .views import UserListView, ClientListView, TrainerListView, ClientProfileView, AssignedClientsView

urlpatterns = [
    # General User Endpoints
    path('users/', UserListView.as_view(), name='user-list'),

    # Client Endpoints
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('clients/profile/', ClientProfileView.as_view(), name='client-profile'),

    # Trainer Endpoints
    path('trainers/', TrainerListView.as_view(), name='trainer-list'),
    path('trainers/assigned-clients/', AssignedClientsView.as_view(), name='assigned-clients'),
]
