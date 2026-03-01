#from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Cart, CartItem
from rest_framework import status
from .serializers import CartSerializer, UpdateCartItemSerializer
from catalog.models import Product


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        product = get_object_or_404(Product, id=product_id)

        if product.stock < quantity:
            return Response({"error": "Not enough stock"}, status=400)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product
        )

        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity

        item.save()

        return Response({"success": True})
    

    #adding update cart item view

class UpdateCartItemView(APIView):
     permission_classes = [IsAuthenticated]

     def patch(self, request):
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item_id = serializer.validated_data["item_id"]
        quantity = serializer.validated_data["quantity"]

        try:
            cart_item = CartItem.objects.get(
                id=item_id,
                cart__user=request.user
            )
        except CartItem.DoesNotExist:
            return Response(
                {"detail": "Cart item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        cart_item.quantity = quantity
        cart_item.save()

        return Response({"detail": "Quantity updated successfully"})


class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")

        cart = get_object_or_404(Cart, user=request.user)

        CartItem.objects.filter(cart=cart, product_id=product_id).delete()

        return Response({"success": True})


class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()
        return Response({"success": True})