from apps.generic.fields import ChoiceDisplayField
from apps.storage.serializers import ImageSerializer
from apps.users.serializers.profile import UserSerializer
from rest_framework import serializers

from .models import News


class NewsItemSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    creator = UserSerializer()
    news_type = ChoiceDisplayField(choices=News.TYPES)
    likes = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    def get_likes(self, obj):
        parent = obj.content_object
        if parent and hasattr(parent, "likes"):
            return parent.likes.all().values_list("pk", flat=True)
        return obj.likes.all().values_list("pk", flat=True)

    def get_views(self, obj):
        parent = obj.content_object
        if parent and hasattr(parent, "views"):
            return parent.views
        return obj.views

    def get_comments_count(self, obj):
        parent = obj.content_object
        if parent and hasattr(parent, "comments_count"):
            return parent.comments_count
        return obj.comments_count

    class Meta:
        model = News
        fields = (
            "pk",
            "news_type",
            "slug",
            "object_id",
            "title",
            "image",
            "creator",
            "description",
            "publish_date",
            "views",
            "likes",
            "comments_count",
            "hash_tags",
        )


class NewsSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    creator = UserSerializer()
    news_type = ChoiceDisplayField(choices=News.TYPES)

    class Meta:
        model = News
        fields = (
            "pk",
            "news_type",
            "slug",
            "object_id",
            "title",
            "image",
            "creator",
            "description",
            "news",
            "publish_date",
            "views",
            "likes",
            "comments_count",
            "hash_tags",
        )


class NewsDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ("pk",)


class NewsLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ("pk", "likes")
        read_only_fields = ("likes",)
