from django.db import models
from django.utils.text import slugify
# Create your models here.
import uuid

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    # Relations
    category = models.ForeignKey("Category", on_delete=models.PROTECT, related_name="products")
    vendor = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="products")

    # Status fields
    is_active = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)  

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4().hex[:12] 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name