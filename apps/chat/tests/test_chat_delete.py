import pytest
from django.conf import settings
from django.urls import reverse

from apps.chat.models import Chat
from apps.chat.tests.factories import ChatFactory
from apps.users.models import User


@pytest.mark.django_db
def test_chat_delete(api_client, user, image):
    chat = ChatFactory(creator=user)
    chat.users.add(user)

    delete_chat_url = reverse("chat:chat-delete", kwargs={"pk": chat.pk})

    response = api_client.patch(delete_chat_url, {})
    assert response.status_code == 403, response.data

    assert api_client.login(username=user.email, password=settings.DEFAULT_PASSWORD)

    response = api_client.patch(delete_chat_url, {})
    assert response.status_code == 403, response.data  # not moderator

    chat.moderators.add(user)
    response = api_client.patch(delete_chat_url, {})
    assert response.status_code == 403, response.data  # guest

    user.role = User.ROLE_MEMBER
    user.save(update_fields=("role",))

    chat.chat_type = Chat.TYPE_CONVERSATION
    chat.save(update_fields=("chat_type",))
    response = api_client.patch(delete_chat_url, {})
    assert response.status_code == 403, response.data  # not for conversation

    chat.chat_type = Chat.TYPE_CHAT_WITH_MODERATORS
    chat.save(update_fields=("chat_type",))
    response = api_client.patch(delete_chat_url, {})
    assert response.status_code == 403, response.data  # not for with moderators

    chat.chat_type = Chat.TYPE_CHAT
    chat.save(update_fields=("chat_type",))

    response = api_client.patch(delete_chat_url, {})
    assert response.status_code == 200, response.data
    deleted_chat = Chat.objects.get(pk=chat.pk)
    assert deleted_chat.is_deleted
