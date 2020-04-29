from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import File, Image


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("name", "file")}),
        (_("Actions"), {"fields": ("creator", "created_date", "updated_date", "is_deleted")}),
    )
    list_display = ("name", "file")
    search_fields = ("name",)
    autocomplete_fields = ("creator",)
    ordering = ("-created_date",)
    readonly_fields = ("created_date", "updated_date")


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("name", "image", "isFromEditor")}),
        (_("Actions"), {"fields": ("creator", "created_date", "updated_date", "is_deleted")}),
    )
    list_display = ("name", "image")
    search_fields = ("name",)
    autocomplete_fields = ("creator",)
    ordering = ("-created_date",)
    readonly_fields = ("created_date", "updated_date")
