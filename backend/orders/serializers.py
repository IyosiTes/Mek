from rest_framework import serializers
from .models import Order, OrderItem

class CreateOrderSerializer(serializers.ModelSerializer):
    payment_method = serializers.ChoiceField(
        choices=["cod", "telebirr"]
    )
    delivery_address = serializers.CharField(max_length = 200)
    class Meta:
        model = Order
        fields = ["payment_method", "delivery_address"]

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name")

    class Meta:
        model = OrderItem
        fields = ["product_name", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "payment_method",
            "payment_status",
            "total_amount",
            "status",
            "items",
        ] 