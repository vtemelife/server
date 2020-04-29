from django.urls import path

from .views import (
    MembershipRequestCreateView,
    MembershipRequestDeleteView,
    MembershipRequestListView,
    MembershipRequestUpdateView,
)

app_name = "apps.memberships"

urlpatterns = [
    path("list/", MembershipRequestListView.as_view(), name="membership-request-list"),
    path("create/", MembershipRequestCreateView.as_view(), name="membership-request-create"),
    path("update/<uuid:pk>/", MembershipRequestUpdateView.as_view(), name="membership-request-update"),
    path("delete/<uuid:pk>/", MembershipRequestDeleteView.as_view(), name="membership-request-delete"),
]
