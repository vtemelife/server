from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "content_type",
                    "object_id",
                    "creator",
                    "theme",
                    "is_whisper",
                    "title",
                    "slug",
                    "image",
                    "description",
                    "post",
                    "hash_tags",
                    "likes",
                    "views",
                )
            },
        ),
        (_("Moderation"), {"fields": ("status",)}),
        (_("Actions"), {"fields": ("created_date", "updated_date", "is_deleted")}),
    )
    list_display = ("title", "content_type", "content_object", "status")
    list_filter = ("content_type", "theme", "status", "is_deleted")
    search_fields = ("title",)
    autocomplete_fields = ("creator", "likes")
    ordering = ("-created_date",)
    readonly_fields = ("created_date", "updated_date")
