# File: backend/users/filters.py

import django_filters
from .models import Client, Trainer


class ClientFilter(django_filters.FilterSet):
    training_status = django_filters.ChoiceFilter(choices=Client.TRAINING_STATUS_CHOICES)
    trainer = django_filters.CharFilter(field_name='trainer__display_name', lookup_expr='icontains')

    class Meta:
        model = Client
        fields = ['training_status', 'trainer']


class TrainerFilter(django_filters.FilterSet):
    employment_status = django_filters.ChoiceFilter(choices=Trainer.EMPLOYMENT_STATUS_CHOICES)

    class Meta:
        model = Trainer
        fields = ['employment_status']
