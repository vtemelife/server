from apps.generic.permissions import IsAuthenticatedAndActive
from django.core.exceptions import PermissionDenied
from django.db.models import F, Q
from rest_framework import generics

from .filtersets import NewsFilterSet
from .models import News
from .serializers import NewsDeleteSerializer, NewsItemSerializer, NewsLikeSerializer, NewsSerializer


class NewsListView(generics.ListAPIView):
    serializer_class = NewsItemSerializer
    queryset = News.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)
    filterset_class = NewsFilterSet
    search_fields = ("title", "description")

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(Q(recipients__isnull=True) | Q(recipients=self.request.user))
        qs = qs.filter(Q(theme__isnull=True) | Q(theme__in=self.request.user.relationship_themes))
        return qs.published().distinct()

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        qs.do_read(self.request.user)
        return qs.order_by("-updated_date")


class NewsRetrieveView(generics.RetrieveAPIView):
    serializer_class = NewsSerializer
    queryset = News.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(Q(recipients__isnull=True) | Q(recipients=self.request.user))
        return qs.published()

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        obj.views += 1
        News.objects.filter(pk=obj.pk).update(views=F("views") + 1)
        return obj


class NewsDeleteView(generics.UpdateAPIView):
    serializer_class = NewsDeleteSerializer
    queryset = News.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)

    def check_object_permissions(self, request, obj):
        if obj.creator_id != request.user.pk:
            raise PermissionDenied

    def perform_update(self, serializer):
        return serializer.save(is_deleted=True)


class NewsLikeView(generics.UpdateAPIView):
    serializer_class = NewsLikeSerializer
    queryset = News.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticatedAndActive,)

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.likes.filter(pk=self.request.user.pk):
            instance.likes.remove(self.request.user)
        else:
            instance.likes.add(self.request.user)
        return instance
