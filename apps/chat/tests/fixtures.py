import pytest
from apps.chat.tests.factories import ChatFactory, MessageFactory


@pytest.fixture
def chat():
    return ChatFactory(name="chat")


@pytest.fixture
def message():
    return MessageFactory(message="test message")
