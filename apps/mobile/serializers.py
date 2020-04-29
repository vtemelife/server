from rest_framework import serializers

from .models import MobileVersion


class VersionSerializer(serializers.ModelSerializer):
    android_apk = serializers.SerializerMethodField()

    def get_android_apk(self, obj):
        return obj.android_apk.url

    class Meta:
        model = MobileVersion
        fields = ("pk", "version", "android_apk", "readme")
