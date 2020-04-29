import pytest
from django.conf import settings
from django.urls import reverse


@pytest.mark.django_db
def test_sign_in_email(api_client, user):
    assert api_client.login(username=user.email, password=settings.DEFAULT_PASSWORD)


@pytest.mark.django_db
def test_sign_in_slug(api_client, user):
    assert api_client.login(username=user.slug, password=settings.DEFAULT_PASSWORD)


@pytest.mark.django_db
def test_sign_in_url(api_client, user):
    sign_in_url = reverse("users:sign-in")

    body = {"email_or_slug": user.slug, "password": settings.DEFAULT_PASSWORD}
    response = api_client.post(sign_in_url, body)
    assert response.status_code == 200, response.data

    body = {"email_or_slug": user.email, "password": settings.DEFAULT_PASSWORD}
    response = api_client.post(sign_in_url, body)
    assert response.status_code == 200, response.data

    body = {"email_or_slug": user.email, "password": "invalid"}
    response = api_client.post(sign_in_url, body)
    assert response.status_code == 400, response.data

    body = {"email_or_slug": "invalid", "password": settings.DEFAULT_PASSWORD}
    response = api_client.post(sign_in_url, body)
    assert response.status_code == 400, response.data

    user.is_deleted = True
    user.save(update_fields=("is_deleted",))

    body = {"email_or_slug": user.email, "password": settings.DEFAULT_PASSWORD}
    response = api_client.post(sign_in_url, body)
    assert response.status_code == 400, response.data


@pytest.mark.django_db
def test_sign_in_verify(api_client, user):
    sign_in_verify_url = reverse("users:sign-in-verify")
    response = api_client.get(sign_in_verify_url)
    assert response.status_code == 403, response.data
    assert api_client.login(username=user.email, password=settings.DEFAULT_PASSWORD)
    response = api_client.get(sign_in_verify_url)
    assert response.status_code == 200, response.data
    assert response.data["pk"] == str(user.pk)
    assert response.data["role"] == user.role
    assert response.data["slug"] == user.slug
    assert response.data["name"] == user.name
    assert response.data["email"] == user.email
    assert response.data["is_real"] == user.is_real
    assert response.data["avatar"] is None
    assert response.data["city"] is None
    assert len(response.data["black_list"]) == 0


@pytest.mark.django_db
def test_sign_out(api_client, user):
    assert api_client.login(username=user.slug, password=settings.DEFAULT_PASSWORD)
    sign_out_url = reverse("users:sign-out")

    body = {}
    response = api_client.post(sign_out_url, body)
    assert response.status_code == 200, response.data
