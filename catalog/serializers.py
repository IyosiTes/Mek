from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "image",
            "category",
            "is_available",
        ]

    def get_is_available(self, obj):
        return obj.stock > 0

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    vendor = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "image",
            "category",
            "vendor",
            "stock",
            "is_active",
            "created_at",
            "updated_at",
        ]

    def get_vendor(self, obj):
        if obj.vendor:
            return {"id": obj.vendor.id, "username": obj.vendor.username}
        return None