from django.urls import path
from .views import (
    CartView,
    MergeCartView, 
    RemoveFromCartView,
    AddToCartView,
    RemoveFromCartView,
    ClearCartView,
    UpdateCartItemView )

urlpatterns = [
     
    path("", CartView.as_view(), name='cart'),
    path("add/", AddToCartView.as_view(), name='cart-add'),
    path("remove/", RemoveFromCartView.as_view(), name='cart-remove'),
    path("clear/", ClearCartView.as_view(), name='cart-clear'),
    path("update/", UpdateCartItemView.as_view(), name='cart-update'),
    path("merge/", MergeCartView.as_view(), name='cart-merge'),
  
]