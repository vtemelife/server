import factory
from apps.storage.models import File, Image
from apps.users.tests.factories import UserFactory
from factory import fuzzy


class FileFactory(factory.django.DjangoModelFactory):

    name = fuzzy.FuzzyText(length=200)
    file = factory.django.FileField()
    creator = factory.SubFactory(UserFactory)

    class Meta:
        model = File


class ImageFactory(factory.django.DjangoModelFactory):
    name = fuzzy.FuzzyText(length=200)
    image = factory.django.ImageField()
    creator = factory.SubFactory(UserFactory)

    class Meta:
        model = Image
