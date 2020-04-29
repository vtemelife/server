from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Shop, ShopItem


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("name", "description", "avatar")}),
        (_("Users"), {"fields": ("creator", "moderators")}),
        (_("Info"), {"fields": ("raiting",)}),
        (_("Actions"), {"fields": ("created_date", "updated_date", "status")}),
    )
    search_fields = ("name", "description")
    list_display = ("name", "creator")
    autocomplete_fields = ("creator", "moderators")
    ordering = ("-created_date",)
    readonly_fields = ("created_date", "updated_date")


@admin.register(ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("shop", "name", "description", "image", "price")}),
        (_("Actions"), {"fields": ("created_date", "updated_date", "status")}),
    )
    search_fields = ("name", "description")
    list_display = ("name", "price", "shop")
    autocomplete_fields = ("shop",)
    ordering = ("-created_date",)
    readonly_fields = ("created_date", "updated_date")
