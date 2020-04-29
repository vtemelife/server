from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Club


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("name", "slug", "description", "image", "club_type")}),
        (_("Users"), {"fields": ("creator", "moderators", "users")}),
        (_("Info"), {"fields": ("relationship_theme", "raiting")}),
        (_("Geo"), {"fields": ("city", "address", "geo")}),
        (_("Moderation"), {"fields": ("status",)}),
        (_("Actions"), {"fields": ("created_date", "updated_date", "is_deleted")}),
    )
    search_fields = ("name",)
    list_display = ("name", "status", "creator", "city")
    list_filter = ("club_type", "status", "is_deleted")
    autocomplete_fields = ("creator", "moderators", "users", "city", "image")
    ordering = ("-created_date",)
    readonly_fields = ("created_date", "updated_date")
