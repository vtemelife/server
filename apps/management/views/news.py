from apps.generic.permissions import IsModerator
from apps.management.filtersets.news import NewsFilterSet
from apps.management.serializers.news import (
    NewsCreateSerializer,
    NewsDeleteSerializer,
    NewsDetailSerializer,
    NewsListSerializer,
    NewsUpdateSerializer,
)
from apps.news.models import News
from rest_framework import generics


class NewsListView(generics.ListAPIView):
    serializer_class = NewsListSerializer
    queryset = (
        News.objects.filter(is_deleted=False, news_type=News.TYPE_SITE_NEWS)
        .select_related("creator")
        .order_by("-created_date")
    )
    permission_classes = (IsModerator,)
    filterset_class = NewsFilterSet
    search_fields = ("title",)


class NewsDetailView(generics.RetrieveAPIView):
    serializer_class = NewsDetailSerializer
    queryset = News.objects.filter(is_deleted=False, news_type=News.TYPE_SITE_NEWS)
    permission_classes = (IsModerator,)


class NewsCreateView(generics.CreateAPIView):
    serializer_class = NewsCreateSerializer
    queryset = News.objects.filter(is_deleted=False)
    permission_classes = (IsModerator,)

    def perform_create(self, serializer):
        instance = serializer.save(creator=self.request.user, news_type=News.TYPE_SITE_NEWS)
        instance.do_read(self.request.user)


class NewsUpdateView(generics.UpdateAPIView):
    serializer_class = NewsUpdateSerializer
    queryset = News.objects.filter(is_deleted=False, news_type=News.TYPE_SITE_NEWS)
    permission_classes = (IsModerator,)


class NewsDeleteView(generics.UpdateAPIView):
    serializer_class = NewsDeleteSerializer
    queryset = News.objects.filter(is_deleted=False, news_type=News.TYPE_SITE_NEWS)
    permission_classes = (IsModerator,)

    def perform_update(self, serializer):
        return serializer.save(is_deleted=True)
