from django.urls import path
from .views import MeView, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
   path("register/", RegisterView.as_view(), name="register"),
   path("me/", MeView.as_view()),
   path("login/", TokenObtainPairView.as_view(), name="login"),
   path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
