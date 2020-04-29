import factory
from cities_light.models import City, Country, Region
from factory import fuzzy


class CountryFactory(factory.django.DjangoModelFactory):
    code3 = fuzzy.FuzzyText(length=3)

    class Meta:
        model = Country
        django_get_or_create = ("code3",)


class RegionFactory(factory.django.DjangoModelFactory):

    country = factory.SubFactory(CountryFactory)
    name = fuzzy.FuzzyText(length=32)

    class Meta:
        model = Region
        django_get_or_create = ("country", "name")


class CityFactory(factory.django.DjangoModelFactory):
    id = fuzzy.FuzzyInteger(1, 1000000)
    country = factory.SubFactory(CountryFactory)
    region = factory.SubFactory(RegionFactory)
    name = fuzzy.FuzzyText(length=32)
    population = 0
    timezone = fuzzy.FuzzyText(length=40)

    class Meta:
        model = City
        django_get_or_create = ("country", "region", "name", "id")
