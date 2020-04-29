from django.urls import path

from .views import ClubCreateView, ClubDeleteView, ClubLeaveView, ClubListView, ClubRetrieveView, ClubUpdateView

app_name = "apps.clubs"

urlpatterns = [
    path("", ClubListView.as_view(), name="club-list"),
    path("create/", ClubCreateView.as_view(), name="club-create"),
    path("<slug:slug>/detail/", ClubRetrieveView.as_view(), name="club-retrieve"),
    path("<slug:slug>/update/", ClubUpdateView.as_view(), name="club-update"),
    path("<slug:slug>/delete/", ClubDeleteView.as_view(), name="club-delete"),
    path("<slug:slug>/leave/", ClubLeaveView.as_view(), name="club-leave"),
]
