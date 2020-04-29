from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import BlackList, User, UserLink, UserOnline


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Profile info"),
            {
                "fields": (
                    "name",
                    "slug",
                    "phone",
                    "skype",
                    "gender",
                    "birthday",
                    "birthday_second",
                    "city",
                    "relationship_formats",
                    "relationship_themes",
                    "about",
                )
            },
        ),
        (_("Social links"), {"fields": ("social_links",)}),
        (_("Friends"), {"fields": ("friends",)}),
        (_("Role"), {"fields": ("role",)}),
        (_("Real"), {"fields": ("status", "is_real", "approver")}),
        (_("Important dates"), {"fields": ("created_date", "updated_date", "last_login")}),
        (
            _("Access and Permissions"),
            {
                "fields": (
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "is_deleted",
                    "groups",
                    "user_permissions",
                    "signup_key",
                    "reset_password_key",
                    "privacy",
                )
            },
        ),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),)
    list_display = (
        "name",
        "email",
        "slug",
        "created_date",
        "is_real",
        "is_active",
        "geo",
        "role",
        "signup_key",
        "reset_password_key",
    )
    list_filter = ("is_real", "is_active", "is_deleted", "role", "is_superuser")
    search_fields = (
        "pk",
        "email",
        "slug",
        "name",
        "city__name",
        "city__alternate_names",
        "city__region__name",
        "city__region__alternate_names",
        "city__country__name",
        "city__country__alternate_names",
    )
    ordering = ("-created_date",)
    autocomplete_fields = ("approver", "city", "friends")
    readonly_fields = ("created_date", "updated_date")


@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    list_display = ("creator", "user", "reason", "reason_message")
    autocomplete_fields = ("creator", "user")
    ordering = ("-created_date",)
    readonly_fields = ("created_date", "updated_date")
    list_filter = ("reason",)
    search_fields = (
        "creator__email",
        "creator__pk",
        "creator__slug",
        "creator__name",
        "user__email",
        "user__pk",
        "user__slug",
        "user__name",
    )


@admin.register(UserLink)
class UserLinkAdmin(admin.ModelAdmin):
    list_display = ("user", "link", "description", "favicon")
    autocomplete_fields = ("user",)
    ordering = ("-created_date",)
    readonly_fields = ("created_date", "updated_date")
    search_fields = ("user__email", "user__pk", "user__slug", "user__name")


@admin.register(UserOnline)
class UserOnlineAdmin(admin.ModelAdmin):
    list_display = ("user", "last_seen", "online")
    autocomplete_fields = ("user",)
    ordering = ("-last_seen",)
    search_fields = ("user__email", "user__pk", "user__slug", "user__name")
