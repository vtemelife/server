from django.contrib import admin

from .models import MobileVersion


@admin.register(MobileVersion)
class MobileVersionAdmin(admin.ModelAdmin):
    list_display = ("version", "android_apk")
    search_fields = ("version",)
    ordering = ("-created_date",)
    readonly_fields = ("created_date", "updated_date")
