from apps.generic.permissions import IsAuthenticatedAndActive
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import MultiPartParser

from .models import File, Image
from .serializers import FileCreateSerializer, ImageCreateSerializer, ImageUploadSerializer


class FileCreateView(generics.CreateAPIView):
    serializer_class = FileCreateSerializer
    permission_classes = (IsAuthenticatedAndActive,)
    parser_classes = (MultiPartParser,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class FileDeleteView(generics.DestroyAPIView):
    queryset = File.objects.all()
    permission_classes = (IsAuthenticatedAndActive,)

    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(creator=self.request.user)
        return qs


class ImageCreateView(generics.CreateAPIView):
    serializer_class = ImageCreateSerializer
    parser_classes = (MultiPartParser,)

    def perform_create(self, serializer):
        user = None
        if self.request.user.is_authenticated:
            user = self.request.user
        serializer.save(creator=user)


class ImageDeleteView(generics.DestroyAPIView):
    queryset = Image.objects.all()
    permission_classes = (IsAuthenticatedAndActive,)

    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(creator=self.request.user)
        return qs


class NoCSRFSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class ImageUploadView(generics.CreateAPIView):
    serializer_class = ImageUploadSerializer
    parser_classes = (MultiPartParser,)
    authentication_classes = (NoCSRFSessionAuthentication,)
    permission_classes = (IsAuthenticatedAndActive,)

    def perform_create(self, serializer):
        user = None
        if self.request.user.is_authenticated:
            user = self.request.user
        serializer.save(creator=user, isFromEditor=True)

    #     return JsonResponse({
    #     'fileName': "2019-08-09 14_49_09(1).jpg",
    #     'uploaded': 1,
    #     'url': "https://ckeditor.com/apps/ckfinder/userfiles/files/2019-08-09%2014_49_09(1).jpg",
    # })
