from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from accounts.serializers import RegisterSerializer,UserSerializer
# Create your views here.
class MeView(APIView):
    permission_classes = [IsAuthenticated]

   
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED
            )
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user =request.user
        return Response({
            "username": user.username,
            "phone_number": user.phone_number,
            "address": user.address,
        }) 
    
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "phone_number": user.phone_number,
            "address": user.address,
        })
