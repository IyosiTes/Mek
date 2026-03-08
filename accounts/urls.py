from django.urls import path
from .views import MeView

urlpatterns = [
   path("auth/me",MeView.as_view()) 

]
