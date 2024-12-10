# File: backend/users/serializers.py

from rest_framework import serializers
from .models import User, Client, Trainer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "username", "email", "display_name", "is_trainer", "is_client",
            "phone_number", "mobile_number", "alternate_phone", "fax", "website",
            "billing_address_line1", "billing_address_line2", "billing_city",
            "billing_state", "billing_postal_code", "billing_country",
            "shipping_address_line1", "shipping_address_line2", "shipping_city",
            "shipping_state", "shipping_postal_code", "shipping_country",
        ]


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    trainer = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_trainer=True),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Client
        fields = [
            "id", "user", "training_status", "personal_training_rate_1_1",
            "personal_training_rate_partner", "personal_training_rate_group",
            "trainer", "emergency_contact_name", "emergency_contact_phone",
        ]


class TrainerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Trainer
        fields = [
            "id", "user", "employment_status", "monthly_rate",
            "gym_session_rate", "sessions_handled", "payments_received",
        ]
