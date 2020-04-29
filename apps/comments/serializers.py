from apps.generic.fields import ContentTypeField
from apps.users.serializers.profile import AnonymousSerializer, UserSerializer
from rest_framework import serializers

from .models import Comment


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentItemSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    children = RecursiveField(many=True)

    class Meta:
        model = Comment
        fields = ("pk", "parent", "comment", "likes", "creator", "created_date", "children")


class CommentWhisperSerializer(serializers.ModelSerializer):
    creator = AnonymousSerializer()
    children = RecursiveField(many=True)

    class Meta:
        model = Comment
        fields = ("pk", "parent", "comment", "likes", "creator", "created_date", "children")


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    content_type = ContentTypeField(required=False)
    creator = serializers.SerializerMethodField()

    def get_creator(self, obj):
        content_object = obj.content_object
        serializer_cls = UserSerializer
        if content_object.__class__.__name__ == "Post" and content_object.is_whisper:
            serializer_cls = AnonymousSerializer
        serializer = serializer_cls(obj.creator, context=self.context)
        return serializer.data

    class Meta:
        model = Comment
        fields = ("pk", "parent", "comment", "likes", "creator", "object_id", "content_type")


class CommentDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("pk",)


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("pk", "likes")
        read_only_fields = ("likes",)
