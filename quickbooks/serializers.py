# File: backend/quickbooks/serializers.py

from rest_framework import serializers
from .models import QuickBooksToken

class QuickBooksTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickBooksToken
        fields = ['id', 'user', 'access_token', 'refresh_token', 'realm_id', 'expires_at']
