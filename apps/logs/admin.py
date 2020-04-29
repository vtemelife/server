import logging

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from .models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("colored_msg", "traceback", "created_date_format")
    list_display_links = ("colored_msg",)
    list_filter = ("level",)
    list_per_page = 10

    def colored_msg(self, instance):
        if instance.level in [logging.NOTSET, logging.INFO]:
            color = "green"
        elif instance.level in [logging.WARNING, logging.DEBUG]:
            color = "orange"
        else:
            color = "red"
        return format_html('<span style="color: {color};">{msg}</span>', color=color, msg=instance.msg)

    def traceback(self, instance):
        return format_html("<pre><code>{content}</code></pre>", content=instance.trace if instance.trace else "")

    def created_date_format(self, instance):
        return instance.created_date

    colored_msg.short_description = _("Message")
    created_date_format.short_description = _("Create Datetime")
