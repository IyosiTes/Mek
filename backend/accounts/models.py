from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
import uuid
from django.utils import timezone
 
class User(AbstractUser):
    # Extra fields beyond Django's default
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=False, null=False)
    church_affiliation = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    # Vendor flag (you control this in admin)
    is_vendor = models.BooleanField(default=False)

    # Preferred payment method (COD or Online)
    PAYMENT_CHOICES = [
        ("COD", "Cash on Delivery"),
        ("ONLINE", "Online Payment"),
    ]
    preferred_payment = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default="COD",
    )

    def __str__(self):
        return self.username
    
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return self.expires_at > timezone.now()   