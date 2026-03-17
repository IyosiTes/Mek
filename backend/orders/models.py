from django.db import models
from django.conf import settings
from catalog.models import Product 
# Create your models here.

class Order(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
    ]

    PAYMENT_STATUS = [
        ("unpaid", "Unpaid"),
        ("submitted", "payment Submitted"),
        ("paid", "Paid"),
    ]

    PAYMENT_METHOD = [
        ("cod", "Cash on Delivery"),
        ("telebirr", "Telebirr"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    order_code = models.CharField(max_length=20, unique=True)

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    #  NEW: structured address
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=255)
    address_details = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="unpaid"
    )

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)

   
    #  NEW: Telebirr support
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_screenshot = models.ImageField(upload_to="payments/", blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"
    
class OrderItem(models.Model):

    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    #price = price at purchase time