from django.urls import path

from .views import (
    PostCreateView,
    PostDeleteView,
    PostLikeView,
    PostListView,
    PostRetrieveView,
    PostToModerateView,
    PostUpdateView,
    WhisperToModerateView,
)

app_name = "apps.posts"

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("create/", PostCreateView.as_view(), name="post-create"),
    path("<slug:slug>/", PostRetrieveView.as_view(), name="post-retrieve"),
    path("<slug:slug>/update/", PostUpdateView.as_view(), name="post-update"),
    path("<slug:slug>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("<slug:slug>/like/", PostLikeView.as_view(), name="post-like"),
    path("<slug:slug>/post-to-moderate/", PostToModerateView.as_view(), name="post-to-moderate"),
    path("<slug:slug>/whisper-to-moderate/", WhisperToModerateView.as_view(), name="whisper-to-moderate"),
]
