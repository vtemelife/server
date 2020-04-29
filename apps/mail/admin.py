from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from apps.mail.models import Email


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ("created_date", "from_email", "to_emails", "subject")
    search_fields = ("from_email", "to_emails", "subject", "body")
    exclude = ("body",)
    readonly_fields = list_display + ("body_html",)
    fieldsets = (
        (_("Users"), {"classes": ("collapse", "close"), "fields": ("from_email", "to_emails")}),
        (_("Body"), {"fields": ("subject", "body_html")}),
    )

    def body_html(self, obj):
        return mark_safe(obj.body)

    def has_add_permission(self, request):
        return False
