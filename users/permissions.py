# File: backend/users/permissions.py

from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsTrainer(BasePermission):
    """
    Allows access only to trainers.
    """
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'trainer_profile')


class IsClient(BasePermission):
    """
    Allows access only to clients.
    """
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'client_profile')
