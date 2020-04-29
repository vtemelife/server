from django.urls import path

from .views import FileCreateView, FileDeleteView, ImageCreateView, ImageDeleteView, ImageUploadView

app_name = "apps.storage"

urlpatterns = [
    path("files/create/", FileCreateView.as_view(), name="files-create"),
    path("files/delete/<uuid:pk>/", FileDeleteView.as_view(), name="files-delete"),
    path("images/create/", ImageCreateView.as_view(), name="images-create"),
    path("images/delete/<uuid:pk>/", ImageDeleteView.as_view(), name="images-delete"),
    path("images/upload/", ImageUploadView.as_view(), name="images-upload"),
]
