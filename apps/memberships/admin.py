from django.contrib import admin

from .models import MembershipRequest


@admin.register(MembershipRequest)
class MembershipRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "content_type", "object_id", "status")
    search_fields = ("user__email", "user__slug", "user__name")
    list_filter = ("content_type", "is_deleted", "status")
    autocomplete_fields = ("user",)
    readonly_fields = ("created_date", "updated_date")
