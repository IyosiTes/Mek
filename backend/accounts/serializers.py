from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "phone_number",
            "email",
            "address",
            "password",
            "password_confirm",
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Passwords do not match")

        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")

        user = User.objects.create_user(
            username=validated_data["username"],
            phone_number=validated_data["phone_number"],
            email=validated_data["email"],
            address=validated_data["address"],
           
            password=validated_data["password"],
        )

        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User;
        fields = [
            "username",
            "phone_number",
            "address",
            "email",
        ]
        read_only_fields = ["username"]
