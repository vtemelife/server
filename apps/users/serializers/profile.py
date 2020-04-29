from apps.chat.models import Chat
from apps.generic.choices import ThemeChoices
from apps.generic.fields import ChoiceDisplayField
from apps.geo.serializers import CitySerializer
from apps.storage.serializers import ImageSerializer
from apps.users.models import User
from apps.users.serializers.mixins import BirthdayMixin, PasswordMixin
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from unidecode import unidecode


class AnonymousSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return _("Anonymous")


class UserSerializer(serializers.ModelSerializer):
    avatar = ImageSerializer()
    city = CitySerializer()
    online = serializers.BooleanField(source="is_online")

    class Meta:
        model = User
        fields = ("pk", "slug", "name", "avatar", "online", "last_seen", "city", "about", "role")


class ProfileSerializer(UserSerializer):
    approver = UserSerializer()

    friends = UserSerializer(many=True)
    online_friends = UserSerializer(many=True)

    role = ChoiceDisplayField(choices=User.ROLES)
    gender = ChoiceDisplayField(choices=User.GENDERS)
    relationship_formats = ChoiceDisplayField(choices=User.FORMATS)
    relationship_themes = ChoiceDisplayField(choices=ThemeChoices.THEMES)

    phone = serializers.SerializerMethodField()
    skype = serializers.SerializerMethodField()

    chat = serializers.SerializerMethodField()
    request = serializers.SerializerMethodField()

    def get_chat(self, obj):
        user = self.context["request"].user
        if user == obj:
            return
        chat = Chat.objects.user_chats(user).filter(chat_type=Chat.TYPE_CONVERSATION, users=obj).first()
        if chat:
            return chat.pk

    def get_request(self, obj):
        user = self.context["request"].user
        request = obj.requests.filter(user=user).first()
        if request:
            return request.pk

    def get_phone(self, obj):
        user = self.context["request"].user
        if user.pk == obj.pk or obj.friends.filter(pk=user.pk).exists():
            return obj.phone

    def get_skype(self, obj):
        user = self.context["request"].user
        if user.pk == obj.pk or obj.friends.filter(pk=user.pk).exists():
            return obj.skype

    class Meta:
        model = User
        fields = (
            "pk",
            "slug",
            "email",
            "name",
            "phone",
            "skype",
            "avatar",
            "birthday",
            "birthday_second",
            "about",
            "online",
            "last_seen",
            "role",
            "is_real",
            "approver",
            "city",
            "friends",
            "online_friends",
            "gender",
            "relationship_formats",
            "relationship_themes",
            "social_links",
            "chat",
            "request",
            "black_list",
        )


class ProfileUpdateSerializer(BirthdayMixin, serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    slug = serializers.SlugField(required=True)
    name = serializers.CharField(required=True)

    def validate_email(self, value):
        if value and User.objects.filter(is_active=True, email=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError(_("User with this email already exists."))
        return value

    def validate_slug(self, value):
        value = slugify(unidecode(value))
        if value and User.objects.filter(is_active=True, slug=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError(_("User with this slug already exists."))
        return value

    def validate(self, data):
        data = super().validate(data)
        errors = {}
        for field in ("city", "gender", "relationship_formats", "relationship_themes", "birthday"):
            if not data.get(field):
                errors[field] = [_("Field is required")]
        if errors:
            raise serializers.ValidationError(errors)
        return data

    class Meta:
        model = User
        fields = (
            "pk",
            "slug",
            "name",
            "email",
            "avatar",
            "city",
            "gender",
            "birthday",
            "birthday_second",
            "relationship_formats",
            "relationship_themes",
            "social_links",
            "about",
            "phone",
            "skype",
            "is_deleted",
        )


class ProfileChangePasswordSerializer(PasswordMixin, serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True)
    repeat_new_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("pk", "slug", "new_password", "repeat_new_password")


class ProfileDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "slug", "is_deleted")


class ProfileGiveRealStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk",)
