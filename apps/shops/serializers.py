from rest_framework import serializers

from .models import Shop


class ShopListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ("pk",)


class ShopRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ("pk",)


class ShopCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ("pk",)


class ShopUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ("pk",)


class ShopDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ("pk",)
