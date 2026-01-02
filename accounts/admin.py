from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Add your custom fields to the default Django UserAdmin
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Extra Info", {
            "fields": (
                "phone_number",
                "church_affiliation",
                "address",
                "is_vendor",
                "preferred_payment",
            )
        }),
    )

    # Control which fields show up in the list view
    list_display = (
        "id",
        "username",
        "email",
        "phone_number",
        "church_affiliation",
        "address",
        "preferred_payment",
        "is_vendor",
        "is_staff",
        "is_superuser",
    )

    # Enable searching by these fields
    search_fields = (
        "username",
        "email",
        "phone_number",
        "church_affiliation",
        "address",
    )

    # Add filters in the right sidebar
    list_filter = (
        "is_vendor",
        "preferred_payment",
        "is_staff",
        "is_superuser",
    )
    from django.contrib import admin

admin.site.site_header = "Mekurab Admin"
admin.site.site_title = "Mekurab Admin Portal"
admin.site.index_title = "Welcome to Mekurab Dashboard"
