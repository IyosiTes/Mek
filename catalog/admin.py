from django.contrib import admin
from .models import Product, Category
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): list_display = ("id", "name")
search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
        "category",
        "price",
        "stock",
        "is_active",
        "vendor",
        "created_at",
    )
    list_filter = ("is_active", "category", "vendor")
    search_fields = ("name", "description", "category__name", "vendor__username")
    prepopulated_fields = {"slug": ("name",)}  # optional
    readonly_fields = ("created_at", "updated_at")

    # Organize fields in admin form
    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "slug", "description", "price", "image", "category")
        }),
        ("Vendor & Stock", {
            "fields": ("vendor", "stock", "is_active")
        }),
        ("Metadata", {
            "fields": ("created_at", "updated_at")
        }),
    )