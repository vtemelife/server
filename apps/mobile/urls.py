from django.urls import path

from .views import VersionRetrieveView

app_name = "apps.posts"

urlpatterns = [path("version/", VersionRetrieveView.as_view(), name="mobile-version-retrieve")]
