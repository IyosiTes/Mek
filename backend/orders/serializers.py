from rest_framework import serializers
from .models import Order, OrderItem

class createOrderSerializer(serializers.ModelSerializer):
    payment_method = serializers.ChoiceField(
        choices=["cod", "telebirr"]
    )
    delivery_address = serializers.CharField(max_length=200)