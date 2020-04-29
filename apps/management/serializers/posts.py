from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.generic.fields import ChoiceDisplayField
from apps.posts.models import Post
from apps.storage.serializers import ImageSerializer
from apps.users.serializers.profile import UserSerializer


class PostListSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    theme = ChoiceDisplayField(choices=Post.THEMES)
    image = ImageSerializer()

    class Meta:
        model = Post
        fields = (
            "pk",
            "slug",
            "image",
            "title",
            "description",
            "theme",
            "likes",
            "views",
            "creator",
            "status",
            "is_ban",
        )


class PostToggleBanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("pk",)


class PostApproveSerializer(serializers.ModelSerializer):
    theme = serializers.ChoiceField(choices=Post.THEMES, required=True, write_only=True)

    def validate(self, attrs):
        if not attrs.get("theme"):
            raise serializers.ValidationError({"theme": [_("Theme is required")]})
        return super().validate(attrs)

    class Meta:
        model = Post
        fields = ("pk", "theme")


class PostDeclineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("pk",)
