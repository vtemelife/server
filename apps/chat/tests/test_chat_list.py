import pytest
from django.conf import settings
from django.urls import reverse

from apps.chat.tests.factories import ChatFactory, MessageFactory
from apps.users.tests.factories import UserFactory


@pytest.mark.django_db
def test_chat_list(api_client, user):
    chat1 = ChatFactory(creator=user)
    chat1.moderators.add(user)
    chat1.users.add(user)
    chat2 = ChatFactory(creator=user)
    chat2.moderators.add(user)
    chat2.users.add(user)

    chat_list_url = reverse("chat:chat-list")
    response = api_client.get(chat_list_url)
    assert response.status_code == 403, response.data

    assert api_client.login(username=user.email, password=settings.DEFAULT_PASSWORD)
    response = api_client.get(chat_list_url)
    assert response.status_code == 200, response.data
    results = response.data["results"]
    assert len(results) == 2
    chat1_result = results[0]
    chat2_result = results[1]

    assert chat1_result["pk"] == str(chat2.pk)
    assert chat2_result["pk"] == str(chat1.pk)


@pytest.mark.django_db
def test_chat_list_order_new_message(api_client, user):
    chat1 = ChatFactory(creator=user)
    chat1.moderators.add(user)
    chat1.users.add(user)
    chat2 = ChatFactory(creator=user)
    chat2.moderators.add(user)
    chat2.users.add(user)

    chat_list_url = reverse("chat:chat-list")
    response = api_client.get(chat_list_url)
    assert response.status_code == 403, response.data

    assert api_client.login(username=user.email, password=settings.DEFAULT_PASSWORD)
    response = api_client.get(chat_list_url)
    assert response.status_code == 200, response.data
    results = response.data["results"]
    assert len(results) == 2
    chat1_result = results[0]
    chat2_result = results[1]

    assert chat1_result["pk"] == str(chat2.pk)
    assert chat2_result["pk"] == str(chat1.pk)

    MessageFactory(chat=chat1, creator=user)
    response = api_client.get(chat_list_url)
    assert response.status_code == 200, response.data
    results = response.data["results"]
    assert len(results) == 2
    chat1_result = results[0]
    chat2_result = results[1]

    assert chat1_result["pk"] == str(chat1.pk)
    assert chat2_result["pk"] == str(chat2.pk)


@pytest.mark.django_db
def test_chat_list_order_new_message_from_other_user(api_client, user):
    other_user = UserFactory()
    chat1 = ChatFactory(creator=user)
    chat1.moderators.add(user)
    chat1.users.add(user)
    chat1.users.add(other_user)
    chat2 = ChatFactory(creator=user)
    chat2.moderators.add(user)
    chat2.users.add(user)
    chat2.users.add(other_user)

    chat_list_url = reverse("chat:chat-list")
    response = api_client.get(chat_list_url)
    assert response.status_code == 403, response.data

    assert api_client.login(username=user.email, password=settings.DEFAULT_PASSWORD)
    response = api_client.get(chat_list_url)
    assert response.status_code == 200, response.data
    results = response.data["results"]
    assert len(results) == 2
    chat1_result = results[0]
    chat2_result = results[1]

    assert chat1_result["pk"] == str(chat2.pk)
    assert chat2_result["pk"] == str(chat1.pk)

    MessageFactory(chat=chat1, creator=other_user)
    response = api_client.get(chat_list_url)
    assert response.status_code == 200, response.data
    results = response.data["results"]
    assert len(results) == 2
    chat1_result = results[0]
    chat2_result = results[1]

    assert chat1_result["pk"] == str(chat1.pk)
    assert chat2_result["pk"] == str(chat2.pk)
