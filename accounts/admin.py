from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("email",)
    list_display = ("email", "full_name", "role", "is_staff", "is_active", "created_at")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    search_fields = ("email", "full_name")
    readonly_fields = ("created_at", "last_login")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name", "contact_number", "profile_photo", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "created_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "full_name", "role", "password1", "password2", "is_staff", "is_superuser"),
            },
        ),
    )

    # No username field (A2)
    filter_horizontal = ("groups", "user_permissions")
