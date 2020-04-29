from django.urls import path

from .views import CommentCreateView, CommentDeleteView, CommentLikeView, CommentListView, CommentUpdateView

app_name = "apps.comments"

urlpatterns = [
    path("list/", CommentListView.as_view(), name="comment-list"),
    path("create/", CommentCreateView.as_view(), name="comment-create"),
    path("<uuid:pk>/update/", CommentUpdateView.as_view(), name="comment-update"),
    path("<uuid:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
    path("<uuid:pk>/like/", CommentLikeView.as_view(), name="comment-like"),
]
