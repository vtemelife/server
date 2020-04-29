from django.urls import path

from .views import (
    MediaCreateView,
    MediaDeleteView,
    MediaFolderCreateView,
    MediaFolderDeleteView,
    MediaFolderListView,
    MediaFolderRetrieveView,
    MediaFolderUpdateView,
    MediaLikeView,
    MediaListView,
    MediaRetrieveView,
    MediaToModerateMediaView,
    MediaUpdateView,
)

app_name = "apps.media"

urlpatterns = [
    path("folder/", MediaFolderListView.as_view(), name="folder-list"),
    path("folder/create/", MediaFolderCreateView.as_view(), name="folder-create"),
    path("folder/<uuid:pk>/", MediaFolderRetrieveView.as_view(), name="folder-retrieve"),
    path("folder/<uuid:pk>/update/", MediaFolderUpdateView.as_view(), name="folder-update"),
    path("folder/<uuid:pk>/delete/", MediaFolderDeleteView.as_view(), name="folder-delete"),
    path("media/", MediaListView.as_view(), name="media-list"),
    path("media/create/", MediaCreateView.as_view(), name="media-create"),
    path("media/<uuid:pk>/", MediaRetrieveView.as_view(), name="media-retrieve"),
    path("media/<uuid:pk>/update/", MediaUpdateView.as_view(), name="media-update"),
    path("media/<uuid:pk>/delete/", MediaDeleteView.as_view(), name="media-delete"),
    path("media/<uuid:pk>/like/", MediaLikeView.as_view(), name="media-like"),
    path("media/<uuid:pk>/to-moderate-media/", MediaToModerateMediaView.as_view(), name="media-to-moderate-media"),
]
