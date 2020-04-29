from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from mptt.admin import MPTTModelAdmin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    fieldsets = (
        (None, {"fields": ("parent", "comment")}),
        (_("Parent"), {"fields": ("content_type", "object_id")}),
        (_("Activity"), {"fields": ("likes",)}),
        (_("Actions"), {"fields": ("creator", "created_date", "updated_date")}),
    )
    list_display = ("preview", "content_type", "content_object")
    list_filter = ("content_type",)
    search_fields = ("comment",)
    autocomplete_fields = ("creator", "parent", "likes")
    mptt_indent_field = "preview"
    mptt_level_indent = 5
    ordering = ("-created_date",)
    readonly_fields = ("created_date", "updated_date")
