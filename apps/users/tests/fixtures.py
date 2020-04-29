import pytest
from apps.users.tests.factories import UserFactory


@pytest.fixture
def user():
    return UserFactory(slug="test", email="test@vteme.com", is_active=True)


@pytest.fixture
def other_user():
    return UserFactory(slug="other_test", email="other_test@vteme.com", is_active=True)
