# File: backend/users/views.py

from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from .models import User, Client, Trainer
from .serializers import UserSerializer, ClientSerializer, TrainerSerializer
from .permissions import IsAdmin, IsTrainer, IsClient


class UserListView(generics.ListAPIView):
    """
    Retrieve a list of all users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class ClientListView(generics.ListCreateAPIView):
    """
    Retrieve and create client records with search and filtering.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsTrainer]

    def get_queryset(self):
        if hasattr(self.request.user, 'trainer_profile'):
            return self.queryset.filter(trainer=self.request.user)
        return super().get_queryset()

    def perform_create(self, serializer):
        """
        Ensure the assigned trainer is valid (if provided).
        """
        trainer = serializer.validated_data.get("trainer")
        if trainer and not trainer.is_trainer:
            raise serializers.ValidationError("Assigned trainer must have a role of trainer.")
        serializer.save()


class ClientProfileView(generics.RetrieveAPIView):
    """
    Retrieve the authenticated client's profile.
    """
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsClient]

    def get_object(self):
        return self.request.user.client_profile


class TrainerListView(generics.ListCreateAPIView):
    """
    Retrieve and create trainer records with search and filtering.
    """
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        """
        Link the trainer with the appropriate user.
        """
        user = serializer.validated_data["user"]
        if not user.is_trainer:
            raise serializers.ValidationError("User must have a role of trainer.")
        serializer.save()


class AssignedClientsView(generics.ListAPIView):
    """
    Retrieve the list of clients assigned to the authenticated trainer.
    """
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsTrainer]

    def get_queryset(self):
        return Client.objects.filter(trainer=self.request.user)
