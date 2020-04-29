from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Party, PartyUser


class PartyUserInline(admin.StackedInline):
    model = PartyUser
    fields = ("user", "status")
    extra = 0
    autocomplete_fields = ("user",)


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    inlines = (PartyUserInline,)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "party_type",
                    "theme",
                    "name",
                    "slug",
                    "image",
                    "status",
                    "short_description",
                    "description",
                    "hash_tags",
                    "likes",
                    "views",
                )
            },
        ),
        (_("Geo"), {"fields": ("geo", "city", "address")}),
        (_("Costs"), {"fields": ("man_cost", "woman_cost", "pair_cost")}),
        (_("Actions"), {"fields": ("created_date", "updated_date", "is_deleted")}),
    )
    list_display = ("name", "status", "theme")
    list_filter = ("party_type", "status", "theme", "is_deleted")
    search_fields = ("name",)
    autocomplete_fields = ("likes", "city", "image")
    ordering = ("-created_date",)
    readonly_fields = ("created_date", "updated_date")
