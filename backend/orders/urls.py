from django.urls import path
from .views import CreateOrderView, OrderDetailView, SubmitTelebirrPaymentView, UserOrdersView

urlpatterns = [
    
     path("", CreateOrderView.as_view()),
    path("<int:pk>/", OrderDetailView.as_view()),
    path("telebirr/<int:order_id>/", SubmitTelebirrPaymentView.as_view()),
    path("list/", UserOrdersView.as_view()),
]