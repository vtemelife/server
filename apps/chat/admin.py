from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Chat, ChatBan, Message


class MessageInline(admin.StackedInline):
    model = Message
    fields = ("message",)
    readonly_fields = ("message",)
    extra = 0


class ChatBanInline(admin.StackedInline):
    model = ChatBan
    fields = ("user", "minutes", "ban_date")
    readonly_fields = ("ban_date",)
    extra = 0


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    inlines = (ChatBanInline, MessageInline)
    fieldsets = (
        (None, {"fields": ("name", "chat_type", "avatar", "creator", "moderators", "users")}),
        (_("Actions"), {"fields": ("created_date", "updated_date", "is_deleted")}),
    )
    list_display = ("chat_name", "chat_type", "created_date", "updated_date")
    list_filter = ("chat_type", "is_deleted")
    search_fields = ("name", "creator__slug", "creator__name")
    autocomplete_fields = ("avatar", "creator", "moderators", "users")
    ordering = ("-created_date",)
    readonly_fields = ("created_date", "updated_date")
