from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("name", "slug", "description", "image", "group_type")}),
        (_("Users"), {"fields": ("creator", "moderators", "users")}),
        (_("Info"), {"fields": ("relationship_theme", "raiting")}),
        (_("Actions"), {"fields": ("created_date", "updated_date", "is_deleted")}),
    )
    search_fields = ("name",)
    list_display = ("name", "creator", "group_type")
    list_filter = ("group_type", "is_deleted")
    autocomplete_fields = ("creator", "moderators", "users", "image")
    ordering = ("-created_date",)
    readonly_fields = ("created_date", "updated_date")
