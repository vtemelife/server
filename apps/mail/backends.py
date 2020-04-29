from django.conf import settings
from sgbackend.mail import SendGridBackend

from .models import Email


class SendgridDatabaseBackend(SendGridBackend):
    def __init__(self, fail_silently=False, **kwargs):
        self.sendgrid_api_key = getattr(settings, "SENDGRID_API_KEY", "")

        if self.sendgrid_api_key:
            super().__init__(fail_silently, **kwargs)

    def write_db_messages(self, emails):
        messages = []

        for message in emails:
            messages.append(
                Email(
                    from_email="%s" % message.from_email,
                    to_emails=", ".join(message.to),
                    subject="%s" % message.subject,
                    body="%s" % message.body,
                )
            )
        Email.objects.bulk_create(messages)

        return len(messages)

    def send_messages(self, emails):
        if self.sendgrid_api_key:
            super().send_messages(emails)

        return self.write_db_messages(emails)
