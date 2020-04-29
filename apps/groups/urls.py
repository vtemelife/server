from django.urls import path

from .views import GroupCreateView, GroupDeleteView, GroupLeaveView, GroupListView, GroupRetrieveView, GroupUpdateView

app_name = "apps.groups"

urlpatterns = [
    path("", GroupListView.as_view(), name="group-list"),
    path("create/", GroupCreateView.as_view(), name="group-create"),
    path("<slug:slug>/detail/", GroupRetrieveView.as_view(), name="group-detail"),
    path("<slug:slug>/update/", GroupUpdateView.as_view(), name="group-update"),
    path("<slug:slug>/delete/", GroupDeleteView.as_view(), name="group-delete"),
    path("<slug:slug>/leave/", GroupLeaveView.as_view(), name="group-leave"),
]
