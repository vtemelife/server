import pytest
from django.conf import settings
from django.urls import reverse


@pytest.mark.django_db
def test_docs_urls(user, api_client):
    """
    Check that the API documentation is rendered without errors
    """
    assert api_client.login(username=user.email, password=settings.DEFAULT_PASSWORD)

    api_docs = reverse("api-docs:docs-index")
    schema_js = reverse("api-docs:schema-js")

    response = api_client.get(api_docs)
    assert response.status_code == 200
    response = api_client.get(schema_js)
    assert response.status_code == 200
