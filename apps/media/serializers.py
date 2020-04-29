from apps.generic.choices import AccessChoices
from apps.generic.fields import ChoiceDisplayField, ContentTypeField
from apps.storage.serializers import ImageSerializer
from apps.users.serializers.profile import UserSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Media, MediaFolder


class MediaFolderItemSerializer(serializers.ModelSerializer):
    show_media = ChoiceDisplayField(choices=AccessChoices.ACCESS)
    media = serializers.SerializerMethodField()

    def get_media(self, obj):
        media = obj.media.filter(media_type=Media.TYPE_PHOTO, is_deleted=False).order_by("views")[:4]
        serializer = MediaItemSerializer(media, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = MediaFolder
        fields = ("pk", "name", "show_media", "creator", "media")


class MediaFolderSerializer(serializers.ModelSerializer):
    show_media = ChoiceDisplayField(choices=AccessChoices.ACCESS)

    class Meta:
        model = MediaFolder
        fields = ("pk", "name", "show_media", "creator")


class MediaFolderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFolder
        fields = ("pk", "name", "show_media")


class MediaFolderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFolder
        fields = ("pk", "name", "show_media")


class MediaFolderDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFolder
        fields = ("pk",)


class MediaItemSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    creator = UserSerializer()

    class Meta:
        model = Media
        fields = (
            "pk",
            "title",
            "description",
            "image",
            "video_code",
            "media_type",
            "hash_tags",
            "views",
            "likes",
            "comments_count",
            "creator",
            "status",
        )


class MediaSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    creator = UserSerializer()
    content_type = ContentTypeField()

    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.get_title()

    class Meta:
        model = Media
        fields = (
            "pk",
            "title",
            "description",
            "image",
            "video_code",
            "media_type",
            "hash_tags",
            "views",
            "likes",
            "comments_count",
            "creator",
            "status",
            "object_id",
            "content_type",
        )


class MediaCreateSerializer(serializers.ModelSerializer):
    content_type = ContentTypeField(required=False)

    def validate(self, data):
        data = super().validate(data)
        if not data.get("image") and not data.get("video_code"):
            raise serializers.ValidationError(_("Please upload image or provide video code"))
        return data

    class Meta:
        model = Media
        fields = (
            "pk",
            "object_id",
            "content_type",
            "title",
            "description",
            "image",
            "video_code",
            "hash_tags",
            "media_type",
        )


class MediaUpdateSerializer(serializers.ModelSerializer):
    content_type = ContentTypeField(required=False)

    class Meta:
        model = Media
        fields = ("pk", "object_id", "content_type", "title", "description", "hash_tags", "video_code")


class MediaDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ("pk",)


class MediaLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ("pk", "likes")
        read_only_fields = ("likes",)


class MediaToModerateMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ("pk",)
