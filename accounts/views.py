from django.shortcuts import render
from rest_framework.views import APIView, Response;
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "email": request.user.email
        })