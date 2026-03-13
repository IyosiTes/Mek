from django.urls import path
from .views import CreateOrderView, OrderDetailView

urlpatterns = [
    
     path("", CreateOrderView.as_view()),
    path("<int:pk>/", OrderDetailView.as_view()),
]