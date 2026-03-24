from rest_framework import serializers
from .models import Order, OrderItem

class CreateOrderSerializer(serializers.Serializer):
    payment_method = serializers.ChoiceField(
        choices=["cod", "telebirr"]
    )
    city = serializers.CharField(max_length=100)
    area = serializers.CharField(max_length=255)
    address_details = serializers.CharField()
    phone_number = serializers.CharField(max_length=20)  

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
            "created_at",
        ] 

class TelebirrPaymentSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(max_length =20)     
    payment_screenshot= serializers.ImageField()   