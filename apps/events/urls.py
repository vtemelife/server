from django.urls import path

from .views import (
    CalendarView,
    MapView,
    PartyApplyView,
    PartyCreateView,
    PartyDeleteView,
    PartyLikeView,
    PartyListView,
    PartyRetrieveView,
    PartyUpdateView,
)

app_name = "apps.events"

urlpatterns = [
    path("", PartyListView.as_view(), name="party-list"),
    path("create/", PartyCreateView.as_view(), name="party-create"),
    path("<slug:slug>/detail/", PartyRetrieveView.as_view(), name="party-retrieve"),
    path("<slug:slug>/update/", PartyUpdateView.as_view(), name="party-update"),
    path("<slug:slug>/delete/", PartyDeleteView.as_view(), name="party-delete"),
    path("<slug:slug>/like/", PartyLikeView.as_view(), name="party-like"),
    path("<slug:slug>/apply/", PartyApplyView.as_view(), name="party-apply"),
    path("map/", MapView.as_view(), name="map"),
    path("calendar/", CalendarView.as_view(), name="calendar"),
]
