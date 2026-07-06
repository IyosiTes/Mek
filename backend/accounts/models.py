from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
import uuid
from django.utils import timezone
 
class User(AbstractUser):
    # Extra fields beyond Django's default
    email = models.EmailField(unique=True)
    
    # Vendor flag (you control this in admin)
    is_vendor = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return self.expires_at > timezone.now()   