from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_code",
        "user",
        "payment_method",
        "payment_status",
        "status",
        "total_amount",
        "created_at",
    )

    list_filter = ("payment_method", "payment_status", "status")

    search_fields = ("order_code", "user__username", "transaction_id")

    inlines = [OrderItemInline]

    readonly_fields = ("order_code", "created_at")

    fieldsets = (
        ("Order Info", {
            "fields": ("order_code", "user", "status", "total_amount")
        }),
        ("Customer Info", {
            "fields": ("full_name", "phone_number")
        }),
        ("Address", {
            "fields": ("city", "area", "address_details")
        }),
        ("Payment", {
            "fields": (
                "payment_method",
                "payment_status",
                "transaction_id",
                "payment_screenshot",
            )
        }),
    )