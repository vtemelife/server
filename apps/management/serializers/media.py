from apps.media.models import Media
from apps.storage.serializers import ImageSerializer
from apps.users.serializers.profile import UserSerializer
from rest_framework import serializers


class MediaListSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    image = ImageSerializer()

    class Meta:
        model = Media
        fields = ("pk", "title", "image", "likes", "views", "creator", "status", "is_ban")


class MediaToggleBanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ("pk",)


class MediaApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ("pk",)


class MediaDeclineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ("pk",)
