from django.urls import path

from .views import CountersView

app_name = "apps.notifications"

urlpatterns = [path("counters/", CountersView.as_view(), name="counters-list")]
