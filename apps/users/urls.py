from django.urls import path

from .views.black_list import BlackListCreateView, BlackListDeleteView, BlackListView
from .views.friends import FriendDeleteView, FriendListView, FriendSearchView
from .views.participants import ParticipantListView
from .views.profile import (
    ProfileChangePasswordView,
    ProfileDeleteView,
    ProfileGiveRealStatusView,
    ProfileUpdateView,
    ProfileView,
)
from .views.reset_password import ResetPasswordStep1View, ResetPasswordStep2View
from .views.sign_in import SignInVerifyView, SignInView, SignOutView
from .views.sign_up import SignUpStep1View, SignUpStep2View

app_name = "apps.users"

urlpatterns = [
    path("sign-in/", SignInView.as_view(), name="sign-in"),
    path("sign-in-verify/", SignInVerifyView.as_view(), name="sign-in-verify"),
    path("sign-out/", SignOutView.as_view(), name="sign-out"),
    path("sign-up/", SignUpStep1View.as_view(), name="sign-up-step1"),
    path("sign-up/step2/<uuid:pk>/", SignUpStep2View.as_view(), name="sign-up-step2"),
    path("reset-password/", ResetPasswordStep1View.as_view(), name="reset-passwords-step1"),
    path("reset-password/step2/<uuid:pk>/", ResetPasswordStep2View.as_view(), name="reset-passwords-step2"),
    path("profile/<slug:slug>/", ProfileView.as_view(), name="profile"),
    path("profile/<slug:slug>/update/", ProfileUpdateView.as_view(), name="profile-update"),
    path("profile/<slug:slug>/password/", ProfileChangePasswordView.as_view(), name="profile-change-password"),
    path("profile/<slug:slug>/delete/", ProfileDeleteView.as_view(), name="profile-delete"),
    path("profile/<slug:slug>/give_real_status/", ProfileGiveRealStatusView.as_view(), name="profile-give-real-status"),
    path("friends/search/", FriendSearchView.as_view(), name="friends-search"),
    path("friends/list/", FriendListView.as_view(), name="friends-list"),
    path("friends/delete/<slug:slug>/", FriendDeleteView.as_view(), name="friends-delete"),
    path("participants/list/", ParticipantListView.as_view(), name="paerticipants-list"),
    path("blacklist/list/", BlackListView.as_view(), name="blacklist-list"),
    path("blacklist/create/", BlackListCreateView.as_view(), name="blacklist-create"),
    path("blacklist/delete/<uuid:pk>/", BlackListDeleteView.as_view(), name="blacklist-delete"),
]
