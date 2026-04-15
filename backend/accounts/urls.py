from django.urls import path
from .views import MeView, RegisterView, UserProfileView, UpdateProfileView, ForgotPasswordView, ResetPasswordView, HealthCheckView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
   path("register/", RegisterView.as_view(), name="register"),
   path("me/", MeView.as_view()),
   path("login/", TokenObtainPairView.as_view(), name="login"),
   path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
   path("profile/", UserProfileView.as_view()),
   path("profile/update/", UpdateProfileView.as_view()),
   path("forgot-password/", ForgotPasswordView.as_view()),
   path("reset-password/", ResetPasswordView.as_view()),
   path("health/", HealthCheckView.as_view()),
]
