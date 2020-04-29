from apps.generic.fields import ChoiceDisplayField, ContentTypeField
from apps.storage.serializers import ImageSerializer
from apps.users.serializers.profile import UserSerializer
from rest_framework import serializers

from .models import Post


class PostItemSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    theme = ChoiceDisplayField(choices=Post.THEMES)

    class Meta:
        model = Post
        fields = (
            "pk",
            "slug",
            "title",
            "image",
            "description",
            "views",
            "likes",
            "comments_count",
            "creator",
            "status",
            "theme",
            "is_whisper",
        )


class PostSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    creator = UserSerializer()

    class Meta:
        model = Post
        fields = (
            "pk",
            "slug",
            "title",
            "image",
            "description",
            "post",
            "views",
            "likes",
            "comments_count",
            "hash_tags",
            "creator",
            "status",
            "theme",
            "is_whisper",
        )


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    content_type = ContentTypeField(required=False)

    class Meta:
        model = Post
        fields = (
            "pk",
            "slug",
            "title",
            "description",
            "image",
            "post",
            "hash_tags",
            "theme",
            "is_whisper",
            "object_id",
            "content_type",
        )


class PostDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("pk", "slug")


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("pk", "likes")
        read_only_fields = ("likes",)


class PostToModerateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("pk",)


class WhisperToModerateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("pk",)
