from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Media, MediaFolder


@admin.register(MediaFolder)
class MediaFolderAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("creator", "name", "show_media")}),
        (_("Actions"), {"fields": ("created_date", "updated_date", "is_deleted")}),
    )
    list_display = ("name", "show_media", "creator")
    list_filter = ("show_media", "is_deleted")
    autocomplete_fields = ("creator",)
    ordering = ("-created_date",)
    readonly_fields = ("created_date", "updated_date")


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "content_type",
                    "object_id",
                    "creator",
                    "title",
                    "description",
                    "media_type",
                    "image",
                    "video_code",
                    "likes",
                    "views",
                )
            },
        ),
        (_("Moderation"), {"fields": ("status",)}),
        (_("Actions"), {"fields": ("created_date", "updated_date", "is_deleted")}),
    )
    list_display = ("title", "content_type", "content_object", "media_type")
    list_filter = ("content_type", "media_type", "status", "is_deleted")
    autocomplete_fields = ("creator", "likes")
    ordering = ("-created_date",)
    readonly_fields = ("created_date", "updated_date")
