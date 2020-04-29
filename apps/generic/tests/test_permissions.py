import pytest
from rest_framework.test import APIRequestFactory


@pytest.mark.django_db
def test_permissions_without_user(is_authenticated_and_active_class_view):
    factory = APIRequestFactory()
    request = factory.get("/")
    response = is_authenticated_and_active_class_view.as_view()(request)
    assert response.status_code == 403


@pytest.mark.django_db
def test_permissions_with_inactive_user(user, is_authenticated_and_active_class_view):
    factory = APIRequestFactory()
    request = factory.get("/")
    user.is_active = False
    user.save(update_fields=["is_active"])
    request.user = user

    response = is_authenticated_and_active_class_view.as_view()(request)
    assert response.status_code == 403


@pytest.mark.django_db
def test_permissions_with_active_user(user, is_authenticated_and_active_class_view):
    factory = APIRequestFactory()
    request = factory.get("/")
    user.is_active = True
    user.save(update_fields=["is_active"])
    request.user = user

    response = is_authenticated_and_active_class_view.as_view()(request)
    assert response.status_code == 200
