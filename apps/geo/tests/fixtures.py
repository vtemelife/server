import pytest

from apps.geo.tests.factories import CityFactory, CountryFactory, RegionFactory


@pytest.fixture
def country():
    return CountryFactory()


@pytest.fixture
def region():
    return RegionFactory()


@pytest.fixture
def city():
    return CityFactory()
