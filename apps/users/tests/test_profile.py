import pytest
from django.conf import settings
from django.urls import reverse

from apps.generic.choices import ThemeChoices
from apps.users.models import User


@pytest.mark.django_db
def test_get_profile(api_client, user):
    profile_url = reverse("users:profile", kwargs={"slug": user.slug})
    response = api_client.get(profile_url)
    assert response.status_code == 403, response.data
    sign_in_url = reverse("users:sign-in")
    body = {"email_or_slug": user.slug, "password": settings.DEFAULT_PASSWORD}
    response = api_client.post(sign_in_url, body)
    assert response.status_code == 200, response.data

    response = api_client.get(profile_url)
    assert response.status_code == 200, response.data
    assert response.data["pk"] == str(user.pk)
    assert response.data["slug"] == user.slug
    assert response.data["name"] == user.name
    assert response.data["email"] == user.email
    assert response.data["avatar"] is None
    assert response.data["phone"] == user.phone
    assert response.data["skype"] == user.skype
    assert response.data["birthday"] == user.birthday
    assert response.data["birthday_second"] == user.birthday_second
    assert response.data["about"] == user.about
    assert response.data["online"] == user.is_online
    assert response.data["last_seen"] <= user.last_seen
    assert response.data["role"]["value"] == user.role
    assert response.data["is_real"] == user.is_real
    assert response.data["approver"] is None
    assert response.data["city"] is None
    assert len(response.data["friends"]) == 0
    assert len(response.data["online_friends"]) == 0
    assert response.data["gender"] == user.gender
    assert response.data["relationship_formats"] == user.relationship_formats
    assert response.data["relationship_themes"] == user.relationship_themes
    assert response.data["social_links"] == user.social_links
    assert response.data["chat"] is None
    assert response.data["request"] is None


@pytest.mark.django_db
def test_get_profile_other_user(api_client, user, other_user):
    sign_in_url = reverse("users:sign-in")
    body = {"email_or_slug": other_user.slug, "password": settings.DEFAULT_PASSWORD}
    response = api_client.post(sign_in_url, body)
    assert response.status_code == 200, response.data

    profile_url = reverse("users:profile", kwargs={"slug": user.slug})

    user.is_active = False
    user.save(update_fields=("is_active",))
    response = api_client.get(profile_url)
    assert response.status_code == 404, response.data

    user.is_active = True
    user.is_deleted = True
    user.save(update_fields=("is_active", "is_deleted"))
    response = api_client.get(profile_url)
    assert response.status_code == 200, response.data

    user.is_active = True
    user.is_deleted = False
    user.save(update_fields=("is_active", "is_deleted"))
    response = api_client.get(profile_url)
    assert response.status_code == 200, response.data

    assert response.data["phone"] is None
    assert response.data["skype"] is None
    assert not response.data["online"]
    assert len(response.data["friends"]) == 0

    other_user.friends.add(user)

    profile_url = reverse("users:profile", kwargs={"slug": user.slug})
    response = api_client.get(profile_url)
    assert response.status_code == 200, response.data
    assert response.data["phone"] == user.phone
    assert response.data["skype"] == user.skype
    assert len(response.data["friends"]) == 1


@pytest.mark.django_db
def test_update_profile(api_client, user, image, city):
    update_profile_url = reverse("users:profile-update", kwargs={"slug": user.slug})

    response = api_client.patch(update_profile_url, {})
    assert response.status_code == 403, response.data

    assert api_client.login(username=user.email, password=settings.DEFAULT_PASSWORD)

    body = {
        "avatar": image.pk,
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

    for required_field in ("city", "gender", "relationship_formats", "relationship_themes", "birthday"):
        new_body = dict(body)
        new_body[required_field] = ""
        response = api_client.patch(update_profile_url, new_body)
        assert response.status_code == 400, response.data

    new_body = dict(body)
    new_body["gender"] = "invalid"
    response = api_client.patch(update_profile_url, new_body)
    assert response.status_code == 400, response.data

    new_body = dict(body)
    new_body["relationship_formats"] = []
    response = api_client.patch(update_profile_url, new_body)
    assert response.status_code == 400, response.data

    new_body = dict(body)
    new_body["relationship_formats"] = ["invalid"]
    response = api_client.patch(update_profile_url, new_body)
    assert response.status_code == 400, response.data

    new_body = dict(body)
    new_body["relationship_themes"] = []
    response = api_client.patch(update_profile_url, new_body)
    assert response.status_code == 400, response.data

    new_body = dict(body)
    new_body["relationship_themes"] = ["invalid"]
    response = api_client.patch(update_profile_url, new_body)
    assert response.status_code == 400, response.data

    user.is_active = False
    user.save(update_fields=("is_active",))
    response = api_client.patch(update_profile_url, body)
    assert response.status_code == 403, response.data

    user.is_active = True
    user.is_deleted = True
    user.save(update_fields=("is_active", "is_deleted"))
    response = api_client.patch(update_profile_url, body)
    assert response.status_code == 404, response.data

    user.is_active = True
    user.is_deleted = False
    user.save(update_fields=("is_active", "is_deleted"))
    response = api_client.patch(update_profile_url, body)
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

    new_body = dict(body)
    new_body["email"] = "new_email@test.com"
    response = api_client.patch(update_profile_url, new_body)
    assert response.status_code == 200, response.data
    assert api_client.login(username="new_email@test.com", password=settings.DEFAULT_PASSWORD)

    new_body = dict(body)
    new_body["slug"] = "new_slug"
    response = api_client.patch(update_profile_url, new_body)
    assert response.status_code == 200, response.data
    assert api_client.login(username="new_slug", password=settings.DEFAULT_PASSWORD)


@pytest.mark.django_db
def test_update_profile_password(api_client, user, image, city):
    update_profile_url = reverse("users:profile-change-password", kwargs={"slug": user.slug})

    response = api_client.patch(update_profile_url, {})
    assert response.status_code == 403, response.data

    assert api_client.login(username=user.email, password=settings.DEFAULT_PASSWORD)

    body = {"new_password": "new_password", "repeat_new_password": "new_password"}

    for required_field in ("new_password", "repeat_new_password"):
        new_body = dict(body)
        new_body[required_field] = ""
        response = api_client.patch(update_profile_url, new_body)
        assert response.status_code == 400, response.data

    user.is_active = False
    user.save(update_fields=("is_active",))
    response = api_client.patch(update_profile_url, body)
    assert response.status_code == 403, response.data

    user.is_active = True
    user.is_deleted = True
    user.save(update_fields=("is_active", "is_deleted"))
    response = api_client.patch(update_profile_url, body)
    assert response.status_code == 404, response.data

    user.is_active = True
    user.is_deleted = False
    user.save(update_fields=("is_active", "is_deleted"))
    response = api_client.patch(update_profile_url, body)
    assert response.status_code == 200, response.data
    assert api_client.login(username=user.slug, password=new_body["new_password"])


@pytest.mark.django_db
def test_delete_profile(api_client, user):
    delete_profile_url = reverse("users:profile-delete", kwargs={"slug": user.slug})
    body = {}
    response = api_client.patch(delete_profile_url, body)
    assert response.status_code == 403, response.data

    assert api_client.login(username=user.email, password=settings.DEFAULT_PASSWORD)
    response = api_client.patch(delete_profile_url, body)
    assert response.status_code == 200, response.data

    user = User.objects.filter(slug=user.slug).first()
    assert user is not None
    assert not user.is_active
    assert user.is_deleted

    assert not api_client.login(username=user.email, password=settings.DEFAULT_PASSWORD)


@pytest.mark.django_db
def test_give_real_status(api_client, user, other_user):
    real_status_url = reverse("users:profile-give-real-status", kwargs={"slug": other_user.slug})
    body = {}
    response = api_client.patch(real_status_url, body)
    assert response.status_code == 403, response.data

    assert api_client.login(username=user.email, password=settings.DEFAULT_PASSWORD)

    # not real and not member
    response = api_client.patch(real_status_url, body)
    assert response.status_code == 403, response.data

    user.role = User.ROLE_MEMBER
    user.is_real = True
    user.save(update_fields=("is_real", "role"))
    response = api_client.patch(real_status_url, body)
    assert response.status_code == 200, response.data

    other_user = User.objects.filter(slug=other_user.slug).first()
    assert other_user is not None
    assert other_user.approver.pk == user.pk
    assert not other_user.is_real  # need to approve from moderators

    other_user.is_real = True
    other_user.save(update_fields=("is_real",))
    response = api_client.patch(real_status_url, body)
    assert response.status_code == 403, response.data

    own_real_status_url = reverse("users:profile-give-real-status", kwargs={"slug": user.slug})
    response = api_client.patch(own_real_status_url, body)
    assert response.status_code == 403, response.data
