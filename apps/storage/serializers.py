import logging

from rest_framework import serializers
from rest_framework.fields import FileField, ImageField

from .models import Image

logger = logging.getLogger("django")


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    thumbnail_100x100 = serializers.SerializerMethodField()
    thumbnail_500x500 = serializers.SerializerMethodField()
    thumbnail_blur_100x100 = serializers.SerializerMethodField()
    thumbnail_blur_500x500 = serializers.SerializerMethodField()

    def get_image(self, obj):
        return obj.get_image_url("image")

    def get_thumbnail_100x100(self, obj):
        return obj.get_image_url("thumbnail_100x100")

    def get_thumbnail_500x500(self, obj):
        return obj.get_image_url("thumbnail_500x500")

    def get_thumbnail_blur_100x100(self, obj):
        return obj.get_image_url("thumbnail_blur_100x100")

    def get_thumbnail_blur_500x500(self, obj):
        return obj.get_image_url("thumbnail_blur_500x500")

    class Meta:
        model = Image
        fields = (
            "pk",
            "image",
            "thumbnail_100x100",
            "thumbnail_500x500",
            "thumbnail_blur_100x100",
            "thumbnail_blur_500x500",
        )


class FileCreateSerializer(serializers.ModelSerializer):
    file = FileField(required=True)

    def create(self, validated_data):
        validated_data["name"] = validated_data.get("file")._name
        return super().create(validated_data)

    class Meta:
        model = Image
        fields = ("pk", "file")


class ImageCreateSerializer(ImageSerializer):
    image = ImageField(required=True)

    def create(self, validated_data):
        validated_data["name"] = validated_data.get("image")._name
        return super().create(validated_data)


class ImageUploadSerializer(serializers.ModelSerializer):
    upload = ImageField(source="image", required=True)
    url = serializers.SerializerMethodField()
    uploaded = serializers.SerializerMethodField()
    fileName = serializers.SerializerMethodField()

    def get_url(self, obj):
        file_obj = obj.image
        try:
            if not file_obj:
                return None
        except FileNotFoundError as e:
            logger.error("File does not exist on filesystem ", exc_info=e)
            return None
        return file_obj.url

    def get_uploaded(self, obj):
        file_obj = obj.image
        try:
            if not file_obj:
                return 0
        except FileNotFoundError as e:
            logger.error("File does not exist on filesystem ", exc_info=e)
            return 0
        return 1

    def get_fileName(self, obj):
        return obj.name

    def create(self, validated_data):
        validated_data["name"] = validated_data.get("image")._name
        return super().create(validated_data)

    class Meta:
        model = Image
        fields = ("pk", "upload", "url", "uploaded", "fileName")
