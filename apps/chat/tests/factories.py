import factory
from apps.chat.models import Chat, Message
from apps.users.tests.factories import UserFactory
from factory import fuzzy


class ChatFactory(factory.django.DjangoModelFactory):
    name = fuzzy.FuzzyText(length=100)

    class Meta:
        model = Chat
        django_get_or_create = ("name",)


class MessageFactory(factory.django.DjangoModelFactory):
    chat = factory.SubFactory(ChatFactory)
    message = fuzzy.FuzzyText(length=100)
    creator = factory.SubFactory(UserFactory)

    class Meta:
        model = Message
