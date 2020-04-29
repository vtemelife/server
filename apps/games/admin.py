from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Game, GameUser


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "creator",
                    "name",
                    "slug",
                    "image",
                    "description",
                    "rules",
                    "token",
                    "hash_tags",
                    "likes",
                    "views",
                )
            },
        ),
        (_("Moderation"), {"fields": ("status",)}),
        (_("Actions"), {"fields": ("created_date", "updated_date", "is_deleted")}),
    )
    list_display = ("name", "creator", "status", "views")
    list_filter = ("status", "is_deleted")
    autocomplete_fields = ("creator", "likes")
    search_fields = ("name",)
    ordering = ("-created_date",)
    readonly_fields = ("created_date", "updated_date")


@admin.register(GameUser)
class GameUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("user", "game", "game_data")}),
        (_("Actions"), {"fields": ("created_date", "updated_date", "is_deleted")}),
    )
    list_display = ("user", "game")
    list_filter = ("is_deleted",)
    search_fields = ("user__email", "user__slug", "user__name", "user__pk")
    autocomplete_fields = ("user", "game")
    ordering = ("-created_date",)
    readonly_fields = ("created_date", "updated_date")
