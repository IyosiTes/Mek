import token
import threading
from .utils.email import send_reset_email
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import  Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import User, PasswordResetToken
from django.contrib.auth.hashers import make_password

from accounts.serializers import (
    RegisterSerializer,
    UserSerializer,
)
# Create your views here.
class MeView(APIView):
    permission_classes = [IsAuthenticated]

   
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                "message": "If this email exists, a reset link was sent"
            })

        token = PasswordResetToken.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(minutes=15)
        )

        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token.token}"

        # background email send
        threading.Thread(
            target=send_reset_email,
            args=(email, reset_link)
        ).start()

        return Response({
            "message": "If this email exists, a reset link was sent"
        })
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        token = request.data.get("token")
        new_password = request.data.get("password")

        try:
            reset_obj = PasswordResetToken.objects.get(token=token)
        except PasswordResetToken.DoesNotExist:
            return Response({"error": "Invalid token"}, status=400)

        if not reset_obj.is_valid():
            return Response({"error": "Token expired"}, status=400)

        user = reset_obj.user
        user.password = make_password(new_password)
        user.save()

        reset_obj.delete()  

        return Response({"message": "Password reset successful"})
    
class HealthCheckView(APIView):
        permission_classes = [AllowAny]
        def get(self, request):
         return Response({
            "status": "ok"
        })