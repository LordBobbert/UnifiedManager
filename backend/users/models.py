from django.db import models

# Create your models here.
# File: backend/users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's built-in User model.
    Includes shared fields for both clients and trainers, aligned with QuickBooks Customer resource.
    """

    # Identification and Metadata
    quickbooks_customer_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    sync_token = models.CharField(max_length=50, null=True, blank=True)  # QuickBooks sync token for versioning

    # Name and Display Information
    display_name = models.CharField(max_length=500, unique=True)  # Must be unique
    title = models.CharField(max_length=16, null=True, blank=True)
    given_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    family_name = models.CharField(max_length=100, null=True, blank=True)
    suffix = models.CharField(max_length=16, null=True, blank=True)
    print_on_cheque_name = models.CharField(max_length=110, null=True, blank=True)

    # Contact Information
    primary_email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    mobile_number = models.CharField(max_length=30, null=True, blank=True)
    alternate_phone = models.CharField(max_length=30, null=True, blank=True)
    fax = models.CharField(max_length=30, null=True, blank=True)
    website = models.URLField(max_length=1000, null=True, blank=True)

    # Address Information
    billing_address_line1 = models.CharField(max_length=255, null=True, blank=True)
    billing_address_line2 = models.CharField(max_length=255, null=True, blank=True)
    billing_city = models.CharField(max_length=100, null=True, blank=True)
    billing_state = models.CharField(max_length=100, null=True, blank=True)
    billing_postal_code = models.CharField(max_length=20, null=True, blank=True)
    billing_country = models.CharField(max_length=100, null=True, blank=True)

    shipping_address_same_as_billing = models.BooleanField(default=True)
    shipping_address_line1 = models.CharField(max_length=255, null=True, blank=True)
    shipping_address_line2 = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=100, null=True, blank=True)
    shipping_state = models.CharField(max_length=100, null=True, blank=True)
    shipping_postal_code = models.CharField(max_length=20, null=True, blank=True)
    shipping_country = models.CharField(max_length=100, null=True, blank=True)

    # Financial Information
    pre_paid_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    opening_balance_date = models.DateField(null=True, blank=True)
    currency = models.CharField(max_length=16, null=True, blank=True)

    # Preferences and Tax Information
    primary_payment_method = models.CharField(max_length=50, null=True, blank=True)
    preferred_delivery_method = models.CharField(max_length=50, null=True, blank=True, choices=[("Print", "Print"), ("Email", "Email"), ("None", "None")])
    taxable = models.BooleanField(default=True)
    tax_exemption_reason = models.TextField(null=True, blank=True)
    resale_number = models.CharField(max_length=16, null=True, blank=True)

    # Sub-Customer and Job Support
    is_sub_customer = models.BooleanField(default=False)
    parent_customer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='sub_customers')
    is_job = models.BooleanField(default=False)

    # Flags
    is_trainer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=True)

    # Notes and Attachments
    notes = models.TextField(max_length=2000, null=True, blank=True)
    attachments = models.JSONField(default=list, blank=True)  # File references stored as JSON

    def __str__(self):
        return self.display_name


class Client(models.Model):
    """
    Additional fields and functionality specific to clients.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile")
    special_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.display_name


class Trainer(models.Model):
    """
    Additional fields and functionality specific to trainers.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="trainer_profile")
    sessions_handled = models.IntegerField(default=0)
    payments_received = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.user.display_name
