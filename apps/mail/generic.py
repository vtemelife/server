from django.conf import settings
from django.template.context import make_context
from django.template.loader import get_template, render_to_string

from .tasks import send_mail_task


class BaseEmail:
    def __init__(self, qs, many=False):
        self.many = many
        self.qs = qs

    def render(self, context=None):
        template = get_template(self.subject)
        subject = template.template.render(make_context(context, autoescape=False))
        subject = "".join(subject.splitlines())

        body = render_to_string(self.body, context)

        return subject, body

    def send(self, context={}):
        context["settings"] = settings
        if self.many is True:
            recipient_emails = list(self.qs.values_list("email", flat=True))
        else:
            recipient_emails = [self.qs.email]

        email_data = {}
        for recipient_email in recipient_emails:
            subject, body = self.render(context)
            email_data[recipient_email] = (subject, body)

        send_mail_task.apply_async((recipient_emails, email_data), countdown=2)
