from apps.users.models import User
from apps.users.serializers.mixins import BirthdayMixin, PasswordMixin
from django.db.models import Q
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from unidecode import unidecode


class SignUpStep1Serializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    slug = serializers.SlugField(required=True)
    name = serializers.CharField(required=True)
    privacy = serializers.BooleanField(required=True)

    def validate_email(self, value):
        if value and User.objects.filter(is_active=True, email=value).exists():
            raise serializers.ValidationError(_("User with this email already exists."))
        return value

    def validate_slug(self, value):
        value = slugify(unidecode(value))
        if value and User.objects.filter(is_active=True, slug=value).exists():
            raise serializers.ValidationError(_("User with this slug already exists."))
        return value

    def validate_privacy(self, value):
        if not value:
            raise serializers.ValidationError(_("Please read privacy."))  # noqa
        return value

    def save(self, **kwargs):
        email = self.validated_data["email"]
        slug = self.validated_data["slug"]
        user = User.objects.filter(is_active=False).filter(Q(email=email) | Q(slug=slug)).first()
        if user:
            self.instance = user
        return super().save(**kwargs)

    class Meta:
        model = User
        fields = ("pk", "slug", "email", "name", "privacy")


class SignUpStep2Serializer(BirthdayMixin, PasswordMixin, serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True)
    repeat_new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        data = super().validate(data)
        errors = {}
        for field in (
            "new_password",
            "repeat_new_password",
            "city",
            "gender",
            "relationship_formats",
            "relationship_themes",
            "birthday",
        ):
            if not data.get(field):
                errors[field] = [_("Field is required")]
        if errors:
            raise serializers.ValidationError(errors)
        return data

    class Meta:
        model = User
        fields = (
            "pk",
            "avatar",
            "new_password",
            "repeat_new_password",
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
        )
