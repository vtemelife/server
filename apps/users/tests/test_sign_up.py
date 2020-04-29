import pytest
from apps.generic.choices import ThemeChoices
from apps.users.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_sign_up_step1(api_client):
    sign_up_step1_url = reverse("users:sign-up-step1")

    body = {"email": "user@test.com", "name": "user", "slug": "user", "privacy": True}
    for required_field in ("email", "name", "slug", "privacy"):
        new_body = dict(body)
        new_body[required_field] = ""
        response = api_client.post(sign_up_step1_url, new_body)
        assert response.status_code == 400

    response = api_client.post(sign_up_step1_url, body)
    assert response.status_code == 201
    user = User.objects.filter(slug="user").first()
    assert user is not None
    assert not user.is_active

    body = {"email": "user@test.com", "name": "new_user", "slug": "new_user", "privacy": True}
    response = api_client.post(sign_up_step1_url, body)
    assert response.status_code == 201, response.data
    new_user = User.objects.filter(slug="new_user").first()
    assert new_user is not None
    assert not new_user.is_active
    assert user.pk == new_user.pk

    body = {"email": "new_user@test.com", "name": "new_user", "slug": "new_user", "privacy": True}
    response = api_client.post(sign_up_step1_url, body)
    assert response.status_code == 201, response.data
    new_new_user = User.objects.filter(email="new_user@test.com").first()
    assert new_new_user is not None
    assert not new_new_user.is_active
    assert new_user.pk == new_new_user.pk

    # emulate step 2
    user.is_active = True
    user.save(update_fields=("is_active",))

    body = {"email": "new_user@test.com", "name": "new_user_repeat", "slug": "new_user_repeat", "privacy": True}
    response = api_client.post(sign_up_step1_url, body)
    assert response.status_code == 400, response.data

    body = {"email": "new_user_repeat@test.com", "name": "new_user", "slug": "new_user", "privacy": True}
    response = api_client.post(sign_up_step1_url, body)
    assert response.status_code == 400, response.data

    assert not api_client.login(username="new_user@test.com", password="123")


@pytest.mark.django_db
def test_sign_up_step2(api_client, image, city):
    sign_up_step1_url = reverse("users:sign-up-step1")

    body_step1 = {"email": "user@test.com", "name": "user", "slug": "user", "privacy": True}
    response = api_client.post(sign_up_step1_url, body_step1)
    assert response.status_code == 201, response.data
    user = User.objects.filter(slug="user").first()
    assert user is not None
    assert not user.is_active

    sign_up_step2_url = reverse("users:sign-up-step2", kwargs={"pk": user.pk})
    body = {
        "avatar": image.pk,
        "new_password": "password",
        "repeat_new_password": "password",
        "city": city.pk,
        "gender": User.GENDER_FAMILY,
        "relationship_formats": [User.FORMAT_SWING_OPEN_SWING],
        "relationship_themes": [ThemeChoices.THEME_SWING],
        "birthday": 1980,
        "birthday_second": 1988,
        "social_links": ["http://test.com"],
        "about": "about",
        "phone": "+79000000000",
        "skype": "skype",
    }

    for required_field in (
        "new_password",
        "repeat_new_password",
        "city",
        "gender",
        "relationship_formats",
        "relationship_themes",
        "birthday",
    ):
        new_body = dict(body)
        new_body[required_field] = ""
        response = api_client.patch(sign_up_step2_url, new_body)
        assert response.status_code == 400, response.data

    new_body = dict(body)
    new_body["gender"] = "invalid"
    response = api_client.patch(sign_up_step2_url, new_body)
    assert response.status_code == 400, response.data

    new_body = dict(body)
    new_body["relationship_formats"] = []
    response = api_client.patch(sign_up_step2_url, new_body)
    assert response.status_code == 400, response.data

    new_body = dict(body)
    new_body["relationship_formats"] = ["invalid"]
    response = api_client.patch(sign_up_step2_url, new_body)
    assert response.status_code == 400, response.data

    new_body = dict(body)
    new_body["relationship_themes"] = []
    response = api_client.patch(sign_up_step2_url, new_body)
    assert response.status_code == 400, response.data

    new_body = dict(body)
    new_body["relationship_themes"] = ["invalid"]
    response = api_client.patch(sign_up_step2_url, new_body)
    assert response.status_code == 400, response.data

    new_body = dict(body)
    new_body["repeat_new_password"] = "invalid"
    response = api_client.patch(sign_up_step2_url, new_body)
    assert response.status_code == 400, response.data

    response = api_client.patch(sign_up_step2_url, body)
    assert response.status_code == 200, response.data
    user = User.objects.filter(pk=user.pk).first()
    assert user is not None
    assert user.avatar.pk == body["avatar"]
    assert user.city.pk == body["city"]
    assert user.gender == body["gender"]
    assert user.relationship_formats == body["relationship_formats"]
    assert user.relationship_themes == body["relationship_themes"]
    assert user.birthday == body["birthday"]
    assert user.birthday_second == body["birthday_second"]
    assert user.birthday_second == body["birthday_second"]
    assert user.social_links == body["social_links"]
    assert user.about == body["about"]
    assert user.phone == body["phone"]
    assert user.skype == body["skype"]

    assert user.is_active
    assert not user.is_email_verified
    assert not user.is_phone_verified
    assert api_client.login(username=body_step1["slug"], password=body["new_password"])
