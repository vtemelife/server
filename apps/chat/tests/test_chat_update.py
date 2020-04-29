import pytest
from apps.chat.models import Chat
from apps.chat.tests.factories import ChatFactory
from apps.users.models import User
from django.conf import settings
from django.urls import reverse


@pytest.mark.django_db
def test_chat_update(api_client, user, image):
    chat = ChatFactory(creator=user)
    chat.users.add(user)

    update_chat_url = reverse("chat:chat-update", kwargs={"pk": chat.pk})

    response = api_client.patch(update_chat_url, {})
    assert response.status_code == 403, response.data

    assert api_client.login(username=user.email, password=settings.DEFAULT_PASSWORD)

    response = api_client.patch(update_chat_url, {})
    assert response.status_code == 403, response.data  # not moderator

    chat.moderators.add(user)
    response = api_client.patch(update_chat_url, {})
    assert response.status_code == 403, response.data  # guest

    user.role = User.ROLE_MEMBER
    user.save(update_fields=("role",))

    chat.chat_type = Chat.TYPE_CONVERSATION
    chat.save(update_fields=("chat_type",))
    response = api_client.patch(update_chat_url, {})
    assert response.status_code == 403, response.data  # not for conversation

    chat.chat_type = Chat.TYPE_CHAT_WITH_MODERATORS
    chat.save(update_fields=("chat_type",))
    response = api_client.patch(update_chat_url, {})
    assert response.status_code == 403, response.data  # not for with moderators

    chat.chat_type = Chat.TYPE_CHAT
    chat.save(update_fields=("chat_type",))

    body = {"name": "new_name", "avatar": image.pk, "moderators": [user.pk], "users": [user.pk]}

    response = api_client.patch(update_chat_url, body)
    assert response.status_code == 200, response.data
    updated_chat = Chat.objects.get(pk=chat.pk)
    assert updated_chat.name == body["name"]
    assert updated_chat.avatar.pk == body["avatar"]
    assert updated_chat.moderators.all().count() == len(body["moderators"])
    assert updated_chat.users.all().count() == len(body["users"])
