from django.urls import path
from .views import MeView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
   path("auth/me/", MeView.as_view()),
   path("auth/login/", TokenObtainPairView.as_view(), name="login"),
   path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
