from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage, get_connection


@shared_task
def send_mail_task(recipients, email_data):
    from_email = settings.DEFAULT_FROM_EMAIL

    connection = get_connection(settings.EMAIL_BACKEND)

    for to in recipients:
        subject, body = email_data[to]

        msg = EmailMessage(subject, body, from_email, [to], reply_to=[to], connection=connection)

        msg.content_subtype = "html"
        msg.send()
