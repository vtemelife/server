from unittest.mock import patch

import pytest
import responses
from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from apps.mail.models import Email
from apps.mail.tasks import send_mail_task
from apps.users.models import User


def send_mail_task_sync(options, **kwargs):
    return send_mail_task.run(*options)


@pytest.mark.django_db
@responses.activate
@patch("apps.mail.tasks.send_mail_task.apply_async", side_effect=send_mail_task_sync)
@override_settings(EMAIL_BACKEND="apps.mail.backends.SendgridDatabaseBackend")
def test_password_reset(m, api_client, user):
    password_reset_url_step1 = reverse("users:reset-passwords-step1")

    data = {"email": ""}
    response = api_client.put(password_reset_url_step1, data)
    assert response.status_code == 400, response.data

    data = {"email": user.email}
    response = api_client.put(password_reset_url_step1, data)
    assert response.status_code == 200, response.data
    assert Email.objects.get(from_email=settings.DEFAULT_FROM_EMAIL, to_emails=user.email)

    user = User.objects.filter(pk=user.pk).first()
    assert user is not None
    assert user.reset_password_key is not None

    password_reset_url_step2 = reverse("users:reset-passwords-step2", kwargs={"pk": user.pk})
    data = {"new_password": "new12345", "repeat_new_password": "", "reset_password_key": user.reset_password_key}
    response = api_client.put(password_reset_url_step2, data)
    assert response.status_code == 400, response.data
    assert not api_client.login(username=user.email, password="new12345")

    data = {"new_password": "", "repeat_new_password": "new12345", "reset_password_key": user.reset_password_key}
    response = api_client.put(password_reset_url_step2, data)
    assert response.status_code == 400, response.data
    assert not api_client.login(username=user.email, password="new12345")

    data = {
        "new_password": "new12345",
        "repeat_new_password": "new123456",
        "reset_password_key": user.reset_password_key,
    }
    response = api_client.put(password_reset_url_step2, data)
    assert response.status_code == 400, response.data
    assert not api_client.login(username=user.email, password="new12345")

    data = {"new_password": "new12345", "repeat_new_password": "new12345", "reset_password_key": ""}
    response = api_client.put(password_reset_url_step2, data)
    assert response.status_code == 400, response.data
    assert not api_client.login(username=user.email, password="new12345")

    data = {"new_password": "new12345", "repeat_new_password": "new12345", "reset_password_key": "invalid123"}
    response = api_client.put(password_reset_url_step2, data)
    assert response.status_code == 400, response.data
    assert not api_client.login(username=user.email, password="new12345")

    data = {
        "new_password": "new12345",
        "repeat_new_password": "new12345",
        "reset_password_key": user.reset_password_key,
    }
    response = api_client.put(password_reset_url_step2, data)
    assert response.status_code == 200, response.data
    assert api_client.login(username=user.email, password="new12345")
