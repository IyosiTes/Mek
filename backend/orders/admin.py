from django.contrib import admin
from .models import Order, OrderItem
from django.utils.html import format_html

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price")
    can_delete = False


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
        "payment_preview",
    )

    list_filter = ("payment_method", "payment_status", "status", "created_at")

    search_fields = ("order_code", "user__username", "phone_number", "transaction_id")

    ordering = ("-created_at",)

    inlines = [OrderItemInline]

    readonly_fields = ("order_code", "created_at", "payment_preview",)

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
                "payment_preview",
            )
        }),
        ("Metadata", {
            "fields": ("created_at",)
        }),
    )

    def payment_preview(self, obj):
        if obj.payment_screenshot:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="height:60px;border-radius:6px;" />'
                '</a>',
                obj.payment_screenshot.url,
                obj.payment_screenshot.url
            )
        return "No Screenshot"

    payment_preview.short_description = "Payment Proof"

    #  ADMIN ACTIONS 
    actions = ["mark_as_paid", "mark_as_rejected", "mark_as_shipped"]

    @admin.action(description="Mark selected orders as PAID")
    def mark_as_paid(self, request, queryset):
        queryset.update(payment_status="paid", status="confirmed")

    @admin.action(description="Mark selected orders as REJECTED")
    def mark_as_rejected(self, request, queryset):
        queryset.update(payment_status="unpaid")

    @admin.action(description="Mark selected orders as SHIPPED")
    def mark_as_shipped(self, request, queryset):
        queryset.update(status="shipped")