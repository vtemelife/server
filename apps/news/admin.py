from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "news_type",
                    "content_type",
                    "object_id",
                    "creator",
                    "recipients",
                    "viewed_by",
                    "hash_tags",
                    "likes",
                    "views",
                )
            },
        ),
        (_("News"), {"fields": ("image", "title", "description", "news")}),
        (_("Actions"), {"fields": ("publish_date", "end_publish_date", "created_date", "updated_date", "is_deleted")}),
    )
    list_display = ("title", "news_type", "content_type", "content_object")
    list_filter = ("news_type", "content_type", "is_deleted")
    ordering = ("-created_date",)
    autocomplete_fields = ("creator", "recipients", "viewed_by", "likes")
    readonly_fields = ("created_date", "updated_date")
