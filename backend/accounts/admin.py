from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("-id",)

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Platform",
            {
                "fields": (
                    "is_vendor",
                )
            },
        ),
    )

    list_display = (
        "id",
        "username",
        "email",
        "is_vendor",
        "is_staff",
        "is_superuser",
        "is_active",
        "last_login",
        "date_joined",
    )

    search_fields = (
        "username",
        "email",
    )

    list_filter = (
        "is_vendor",
        "is_staff",
        "is_superuser",
        "is_active",
    )


admin.site.site_header = "Mekwerab Admin"
admin.site.site_title = "Mekwerab Admin Portal"
admin.site.index_title = "Welcome to Mekwerab Dashboard"
