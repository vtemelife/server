from django.urls import path

from .views import (
    ChatModeratorsSelectView,
    ChatUsersSelectView,
    CitySelectView,
    ClubsSelectView,
    CountrySelectView,
    ModeratorsSelectView,
    RegionSelectView,
)

app_name = "apps.selects"

urlpatterns = [
    path("country/", CountrySelectView.as_view(), name="select-country"),
    path("region/", RegionSelectView.as_view(), name="select-region"),
    path("city/", CitySelectView.as_view(), name="select-city"),
    path("moderators/", ModeratorsSelectView.as_view(), name="select-moderators"),
    path("chat/moderators/", ChatModeratorsSelectView.as_view(), name="select-chat-moderators"),
    path("chat/users/", ChatUsersSelectView.as_view(), name="select-chat-users"),
    path("clubs/", ClubsSelectView.as_view(), name="select-clubs"),
]
