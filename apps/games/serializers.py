from rest_framework import serializers

from apps.storage.serializers import ImageSerializer

from .models import Game, GameUser


class GameItemSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    players_count = serializers.SerializerMethodField()

    def get_players_count(self, obj):
        return obj.game_gameusers.filter(is_deleted=False).count()

    class Meta:
        model = Game
        fields = ("pk", "slug", "name", "image", "description", "views", "likes", "creator", "status", "players_count")


class GameSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    players_count = serializers.SerializerMethodField()
    game_user_pk = serializers.SerializerMethodField()

    def get_players_count(self, obj):
        return obj.game_gameusers.filter(is_deleted=False).count()

    def get_game_user_pk(self, obj):
        request = self.context["request"]
        user = request.user
        try:
            return GameUser.objects.get(user=user, game=obj).pk
        except GameUser.DoesNotExist:
            return None

    class Meta:
        model = Game
        fields = (
            "pk",
            "slug",
            "name",
            "image",
            "description",
            "rules",
            "views",
            "likes",
            "hash_tags",
            "creator",
            "status",
            "players_count",
            "game_user_pk",
        )


class GameUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ("pk", "slug", "name", "image", "description", "rules", "hash_tags")


class GameDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ("pk", "slug")


class GameUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameUser
        fields = ("pk", "game", "game_data")


class GameUserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameUser
        fields = ("pk", "game_data", "updated_date")


class GameUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameUser
        fields = ("pk", "game_data")


class GameUserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameUser
        fields = ("pk",)
