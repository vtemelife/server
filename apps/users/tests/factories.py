import factory
from apps.users.models import User
from django.conf import settings


class UserFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "name-{0}".format(n))
    slug = factory.Sequence(lambda n: "slug-{0}".format(n))
    email = factory.Sequence(lambda n: "user-{0}@example.com".format(n))
    phone = factory.Sequence(lambda n: "+1234{0}".format(n))
    password = factory.PostGenerationMethodCall("set_password", settings.DEFAULT_PASSWORD)

    class Meta:
        model = User
        django_get_or_create = ("email",)
