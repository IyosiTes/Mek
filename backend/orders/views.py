from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework import status

from cart.models import CartItem
from .models import Order, OrderItem
from .serializers import CreateOrderSerializer, OrderSerializer
import uuid


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = request.user
        payment_method = serializer.validated_data["payment_method"]
    

        cart_items = CartItem.objects.filter(cart__user=user)
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        total = 0
        for item in cart_items:
            if item.quantity > item.product.stock:
                return Response(
                    {"error": f"{item.product.name} out of stock"}, status=400
                )
            total += item.total_price

        #  Generate order code
        order_code = f"ETH-{uuid.uuid4().hex[:6].upper()}"

        # Create order
        order = Order.objects.create(
            user=user,
            order_code=order_code,
            full_name=user.username,
            phone_number=user.phone_number,

            city=serializer.validated_data["city"],
            area=serializer.validated_data["area"],
            address_details=serializer.validated_data["address_details"],

            total_amount=total,
            payment_method=payment_method,
        )

        #  Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

            # reduce stock
            item.product.stock -= item.quantity
            item.product.save()

        cart_items.delete()

        return Response(
            {
                "order_id": order.id,
                "order_code": order.order_code,
                "payment_method": order.payment_method,
            },
            status=201,
        )
       

class OrderDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)