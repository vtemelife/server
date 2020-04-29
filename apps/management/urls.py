from django.urls import path

from .views.chats import ChatWithModeratorsAndDevelopersListView
from .views.clubs import ClubApproveView, ClubDeclineView, ClubListView, ClubToggleBanView
from .views.media import MediaApproveView, MediaDeclineView, MediaListView, MediaToggleBanView
from .views.news import NewsCreateView, NewsDeleteView, NewsDetailView, NewsListView, NewsUpdateView
from .views.parties import PartyApproveView, PartyDeclineView, PartyListView, PartyToggleBanView
from .views.posts import PostApproveView, PostDeclineView, PostListView, PostToggleBanView
from .views.users import UserListView, UserSetMemberView, UserSetRealView, UserToggleBanView

app_name = "apps.tasks"

urlpatterns = [
    path(
        "chat_with_moderators_and_developers/",
        ChatWithModeratorsAndDevelopersListView.as_view(),
        name="chat-with-moderators-and-developers-list",
    ),
    path("users/", UserListView.as_view(), name="users-list"),
    path("users/<uuid:pk>/toggle/ban/", UserToggleBanView.as_view(), name="users-toggle-ban"),
    path("users/<uuid:pk>/set/member/", UserSetMemberView.as_view(), name="users-set-member"),
    path("users/<uuid:pk>/set/real/", UserSetRealView.as_view(), name="users-set-real"),
    path("clubs/", ClubListView.as_view(), name="clubs-list"),
    path("clubs/<uuid:pk>/approve/", ClubApproveView.as_view(), name="clubs-approve"),
    path("clubs/<uuid:pk>/decline/", ClubDeclineView.as_view(), name="clubs-decline"),
    path("clubs/<uuid:pk>/toggle/ban/", ClubToggleBanView.as_view(), name="clubs-toggle-ban"),
    path("parties/", PartyListView.as_view(), name="parties-list"),
    path("parties/<uuid:pk>/approve/", PartyApproveView.as_view(), name="parties-approve"),
    path("parties/<uuid:pk>/decline/", PartyDeclineView.as_view(), name="parties-decline"),
    path("parties/<uuid:pk>/toggle/ban/", PartyToggleBanView.as_view(), name="parties-toggle-ban"),
    path("media/", MediaListView.as_view(), name="media-list"),
    path("media/<uuid:pk>/approve/", MediaApproveView.as_view(), name="media-approve"),
    path("media/<uuid:pk>/decline/", MediaDeclineView.as_view(), name="media-decline"),
    path("media/<uuid:pk>/toggle/ban/", MediaToggleBanView.as_view(), name="media-toggle-ban"),
    path("posts/", PostListView.as_view(), name="posts-list"),
    path("posts/<uuid:pk>/approve/", PostApproveView.as_view(), name="posts-approve"),
    path("posts/<uuid:pk>/decline/", PostDeclineView.as_view(), name="posts-decline"),
    path("posts/<uuid:pk>/toggle/ban/", PostToggleBanView.as_view(), name="post-toggle-ban"),
    path("news/", NewsListView.as_view(), name="news-list"),
    path("news/create/", NewsCreateView.as_view(), name="news-create"),
    path("news/detail/<uuid:pk>/", NewsDetailView.as_view(), name="news-detail"),
    path("news/update/<uuid:pk>/", NewsUpdateView.as_view(), name="news-update"),
    path("news/delete/<uuid:pk>/", NewsDeleteView.as_view(), name="news-delete"),
]
