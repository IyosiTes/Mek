from django.urls import path
from .views import CartView, AddToCartView, RemoveFromCartView, ClearCartView

urlpatterns = [
    path("", CartView.as_view(), name='cart'),
    path("add/", AddToCartView.as_view(), name='cart-add'),
    path("remove/", RemoveFromCartView.as_view(), name='cart-remove'),
    path("clear/", ClearCartView.as_view(), name='cart-clear'),
]