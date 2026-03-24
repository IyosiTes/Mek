from django.contrib import admin
from .models import Product, Category
# Register your models here.
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): 
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image_preview",
        "name",
        "category",
        "price",
        "stock",
        "is_active",
        "vendor",
        "created_at",
       
    )
    list_filter = ("is_active", "category", "vendor")
    search_fields = ("name", "description", "category__name", "vendor__username")
    ordering = ("-created_at",)

    list_editable = ("price", "is_active", "stock",)

    list_select_related = ("category", "vendor")
    date_hierarchy = "created_at"
    readonly_fields = ("slug", "created_at", "updated_at", "image_preview")

    # Organize fields in admin form
    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "slug", "description", "price", "stock", "category")
        }),
         ("Image", {
            "fields": ("image", "image_preview")
        }),
       ("Status", {
            "fields": ("is_active", "vendor")
        }),
        ("Metadata", {
            "fields": ("created_at", "updated_at")
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="width:60px;height:60px;border-radius:6px;object-fit:cover;" />'
                '</a>',
                obj.image.url,
                obj.image.url
            )
        return format_html('<span style="color:gray;">No Image</span>')

    image_preview.short_description = "Preview"