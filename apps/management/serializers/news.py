from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.news.models import News
from apps.storage.serializers import ImageSerializer
from apps.users.serializers.profile import UserSerializer


class NewsListSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    creator = UserSerializer()

    class Meta:
        model = News
        fields = ("pk", "title", "image", "creator", "description", "publish_date", "end_publish_date")


class NewsDetailSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    creator = UserSerializer()

    class Meta:
        model = News
        fields = ("pk", "title", "image", "creator", "description", "news", "publish_date", "end_publish_date")


class NewsCreateSerializer(serializers.ModelSerializer):
    publish_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False, allow_null=True)
    end_publish_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False, allow_null=True)

    def validate(self, data):
        data = super().validate(data)
        if (
            data.get("publish_date")
            and data.get("end_publish_date")
            and data.get("publish_date") >= data.get("end_publish_date")
        ):
            raise serializers.ValidationError({"end_publish_date": [_("End publish data has to be > publish data")]})
        return data

    class Meta:
        model = News
        fields = ("pk", "title", "image", "description", "news", "publish_date", "end_publish_date")


class NewsUpdateSerializer(NewsCreateSerializer):
    pass


class NewsDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ("pk",)
