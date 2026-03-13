from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework import status

from cart.models import CartItem
from .models import Order, OrderItem
from .serializers import CreateOrderSerializer, OrderSerializer

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = request.user
        payment_method = serializer.validated_data["payment_method"]
        delivery_address = serializer.validated_data["delivery_address"]

        cart_items = CartItem.objects.filter(cart__user=user)
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        total = 0
        for item in cart_items:
            if not item.product:
                return Response(
                    {"error": f"A product in cart no longer exists"},
                    status=400
                )
            if item.quantity > item.product.stock:
                return Response(
                    {"error": f"{item.product.name} out of stock"},
                    status=400
                )
            total += item.total_price

        # Create order
        order = Order.objects.create(
            user=user,
            total_amount=total,
            payment_method=payment_method,
            delivery_address=delivery_address,
        )

        # Create order items and update stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            item.product.stock -= item.quantity
            item.product.save()

        cart_items.delete()

        return Response({
            "order_id": order.id,
            "payment_method": order.payment_method
        }, status=201)


class OrderDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)