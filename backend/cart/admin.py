

# Register your models here.
from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ("total_price",)  
    autocomplete_fields = ("product",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_items", "total_price", "updated_at")
    list_select_related = ("user",) 
    ordering = ("-updated_at",)
    search_fields = ("user__username", "user__email")
    readonly_fields = ("total_items", "total_price", "created_at", "updated_at")
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity", "total_price")
    list_select_related = ("cart", "product")
    readonly_fields = ("total_price",)
    search_fields = ("cart__user__username", "product__name")
    ordering = ("-id",)