from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Custom user model for gas utility service"""
    CUSTOMER = 'customer'
    SUPPORT = 'support'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (CUSTOMER, _('Customer')),
        (SUPPORT, _('Support Representative')),
        (ADMIN, _('Administrator')),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=CUSTOMER,
    )
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    account_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    
    def __str__(self):
        return self.username
    
    def is_customer(self):
        return self.role == self.CUSTOMER
    
    def is_support(self):
        return self.role == self.SUPPORT
    
    def is_admin_user(self):
        return self.role == self.ADMIN

class CustomerProfile(models.Model):
    """Additional customer information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    service_address = models.TextField()
    billing_address = models.TextField(blank=True)
    meter_number = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

