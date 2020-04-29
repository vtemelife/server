import pytest
from apps.chat.models import Chat
from apps.chat.tests.factories import ChatFactory, MessageFactory
from apps.users.tests.factories import UserFactory


@pytest.mark.django_db
def test_chat_model_managers(api_client, user):
    other_user = UserFactory()
    chat = ChatFactory(creator=user)
    chat.moderators.add(user)
    chat.users.add(user)
    chat.users.add(other_user)

    message = MessageFactory(chat=chat, creator=other_user)
    message.viewed_by.add(other_user)

    chats = Chat.objects.user_chats(user=user)
    assert chats.count() == 1
    assert chats.first().pk == chat.pk

    chats = Chat.objects.user_chats(user=other_user)
    assert chats.count() == 1
    assert chats.first().pk == chat.pk

    chat.chat_type = Chat.TYPE_CHAT_WITH_MODERATORS
    chat.save(update_fields=("chat_type",))
    chats = Chat.objects.user_chats(user=user)
    assert chats.count() == 1  # cause creator
    assert chats.first().pk == chat.pk

    chats = Chat.objects.user_chats(user=other_user)
    assert chats.count() == 0

    chats = Chat.objects.user_chats(user=other_user, is_moderator=True)
    assert chats.count() == 1
    assert chats.first().pk == chat.pk

    chats = Chat.objects.unread(user=user)
    assert chats.count() == 1  # cause creator
    assert chats.first().pk == chat.pk

    chats = Chat.objects.unread(user=other_user)
    assert chats.count() == 0


@pytest.mark.django_db
def test_chat_model_recipients(api_client, user):
    other_user = UserFactory()
    chat = ChatFactory(creator=user)
    chat.moderators.add(user)
    chat.users.add(user)
    chat.users.add(other_user)

    message = MessageFactory(chat=chat, creator=other_user)
    message.viewed_by.add(other_user)

    recipients = chat.get_recipients(sender=user)
    assert len(recipients) == 1
    assert recipients[0] == other_user.name

    other_user.is_deleted = True
    other_user.save(update_fields=("is_deleted",))
    recipients = chat.get_recipients(sender=user)
    assert len(recipients) == 1
    assert recipients[0] == other_user.name

    other_user.is_active = False
    other_user.save(update_fields=("is_active",))
    recipients = chat.get_recipients(sender=user)
    assert len(recipients) == 1
    assert recipients[0] == other_user.name
