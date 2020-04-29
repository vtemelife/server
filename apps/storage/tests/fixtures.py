import pytest
from apps.storage.tests.factories import ImageFactory


@pytest.fixture
def image():
    return ImageFactory()
