import datetime

from apps.generic.choices import ThemeChoices
from apps.generic.models import GenericModelMixin, GenericModerateMixin
from cities_light.models import City
from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils import FieldTracker


class UserQuerySet(models.QuerySet):
    def with_online(self):
        delta = timezone.now() - datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)
        return self.annotate(
            online=models.Case(
                models.When(user_online__last_seen__gte=delta, then=models.Value(1)),
                default=models.Value(0),
                output_field=models.IntegerField(),
            )
        )


class UserManager(BaseUserManager):
    use_in_migrations = True

    def get_by_natural_key(self, email_or_slug):
        if "@" in email_or_slug:
            kwargs = {"email": email_or_slug}
        else:
            kwargs = {"slug": email_or_slug}
        return self.get(**kwargs)

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def with_online(self):
        return self.get_queryset().with_online()


class User(PermissionsMixin, GenericModerateMixin, AbstractBaseUser):
    ROLE_GUEST = "guest"
    ROLE_MEMBER = "member"
    ROLE_ORGANIZER = "organizer"
    ROLE_MODERATOR = "moderator"
    ROLES = (
        (ROLE_GUEST, _("Guest")),
        (ROLE_MEMBER, _("Member")),
        (ROLE_ORGANIZER, _("Organizer")),
        (ROLE_MODERATOR, _("Moderator")),
    )

    GENDER_M = "m"
    GENDER_W = "w"
    GENDER_FAMILY = "family"
    GENDER_MW = "mw"
    GENDER_MM = "mm"
    GENDER_WW = "ww"
    GENDER_TRANS = "trans"
    GENDERS = (
        (GENDER_M, _("M")),
        (GENDER_W, _("W")),
        (GENDER_FAMILY, _("Family")),
        (GENDER_MW, _("MW")),
        (GENDER_MM, _("MM")),
        (GENDER_WW, _("WW")),
        (GENDER_TRANS, _("Trans")),
    )

    STATUS_MARRIED = "married"
    STATUS_DATING = "dating"
    STATUS_SINGLE = "single"
    STATUSES = ((STATUS_MARRIED, _("Married")), (STATUS_DATING, _("Dating")), (STATUS_SINGLE, _("Single")))

    FORMAT_SWING_OPEN_SWING = "open_swing"
    FORMAT_SWING_CLOSE_SWING = "close_swing"
    FORMAT_SWING_SOFT_SWING = "soft_swing"
    FORMAT_SWING_WMW = "wmw"
    FORMAT_SWING_MWM = "mwm"
    FORMAT_SWING_GANGBANG = "gangbang"
    FORMAT_SWING_SEXWIFE = "sexwife"
    FORMAT_SWING_HOTWIFE = "hotwife"
    FORMAT_SWING_CUCKOLD = "cuckold"
    FORMAT_SWING_CUCKQUEEN = "cuckqueen"

    FORMAT_BDSM_TOP = "top"
    FORMAT_BDSM_BOTTOM = "bottom"
    FORMAT_BDSM_SWITCH = "switch"

    FORMAT_LGBT_ACTIVE = "lgbt_active"
    FORMAT_LGBT_PASSIVE = "lgbt_passive"
    FORMAT_LGBT_SWITCH = "lgbt_switch"

    FORMAT_POLIAMORIA = "format_poliamoria"

    FORMAT_VIRT = "format_virt"

    FORMAT_OTHER = "format_other"

    FORMATS = (
        (FORMAT_SWING_OPEN_SWING, _("Open Swing")),
        (FORMAT_SWING_CLOSE_SWING, _("Close Swing")),
        (FORMAT_SWING_SOFT_SWING, _("Soft Swing")),
        (FORMAT_SWING_WMW, _("WMW")),
        (FORMAT_SWING_MWM, _("MWM")),
        (FORMAT_SWING_GANGBANG, _("GangBang")),
        (FORMAT_SWING_SEXWIFE, _("Sexwife")),
        (FORMAT_SWING_HOTWIFE, _("Hotwife")),
        (FORMAT_SWING_CUCKOLD, _("Cuckold")),
        (FORMAT_SWING_CUCKQUEEN, _("Cuckqueen")),
        (FORMAT_BDSM_TOP, _("Top")),
        (FORMAT_BDSM_BOTTOM, _("Bottom")),
        (FORMAT_BDSM_SWITCH, _("Switch")),
        (FORMAT_LGBT_ACTIVE, _("LGBT Active")),
        (FORMAT_LGBT_PASSIVE, _("LGBT Passive")),
        (FORMAT_LGBT_SWITCH, _("LGBT Switch")),
        (FORMAT_POLIAMORIA, _("Poliamoria")),
        (FORMAT_VIRT, _("Virt")),
        (FORMAT_OTHER, _("Other")),
    )

    email = models.EmailField(_("Email"), unique=True, db_index=True)

    name = models.CharField(_("Name"), max_length=150, db_index=True)
    slug = models.SlugField(_("Slug"), max_length=150, db_index=True, unique=True)
    avatar = models.ForeignKey(
        "storage.Image", verbose_name=_("Avatar"), on_delete=models.SET_NULL, null=True, blank=True
    )

    phone = models.CharField(_("Phone"), null=True, blank=True, max_length=64)
    skype = models.CharField(_("Skype"), null=True, blank=True, max_length=64)

    birthday = models.IntegerField(_("Birthday (M, W in WW or trans)"), null=True)
    birthday_second = models.IntegerField(_("Birthday second (W, M in MM)"), null=True, blank=True)

    city = models.ForeignKey(City, verbose_name=_("City"), on_delete=models.CASCADE, null=True)

    gender = models.CharField(_("Gender"), max_length=255, choices=GENDERS, null=True)

    relationship_formats = ArrayField(
        models.CharField(choices=FORMATS, max_length=255), verbose_name=_("Relationship formats"), null=True
    )
    relationship_themes = ArrayField(
        models.CharField(choices=ThemeChoices.THEMES, max_length=255), verbose_name=_("Relationship themes"), null=True
    )

    social_links = ArrayField(models.URLField(), verbose_name=_("Social links"), null=True, blank=True)
    about = RichTextField(_("About"), config_name="basic", null=True, blank=True)

    friends = models.ManyToManyField("self", verbose_name=_("Friends"), related_name="user_friends", blank=True)
    black_list = models.ManyToManyField(
        "self",
        verbose_name=_("Black List"),
        related_name="user_black_list",
        blank=True,
        through="users.BlackList",
        symmetrical=False,
    )

    approver = models.ForeignKey(
        "self",
        verbose_name=_("Approver real status"),
        related_name="approver_real_users",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    role = models.CharField(_("Role"), max_length=16, choices=ROLES, default=ROLE_GUEST)
    is_real = models.BooleanField(_("Real"), default=False)
    is_superuser = models.BooleanField(_("System administrator"), default=False)
    is_staff = models.BooleanField(_("Staff"), default=False)
    is_active = models.BooleanField(_("Active"), default=False)
    is_email_verified = models.BooleanField(_("Is email verified"), default=False)
    is_phone_verified = models.BooleanField(_("Is phone verified"), default=False)

    signup_key = models.PositiveIntegerField(_("SignUp Key"), null=True, blank=True)
    reset_password_key = models.PositiveIntegerField(_("Reset Password Key"), null=True, blank=True)

    privacy = models.BooleanField(_("Privacy"), default=False)

    requests = GenericRelation("memberships.MembershipRequest")

    objects = UserManager()

    fields_tracker = FieldTracker(
        fields=[
            "name",
            "slug",
            "social_links",
            "about",
            "avatar",
            "gender",
            "relationship_formats",
            "relationship_themes",
        ]
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["slug", "name"]

    @property
    def is_online(self):
        if hasattr(self, "online"):
            return bool(self.online)
        try:
            return self.user_online.online
        except ObjectDoesNotExist:
            return False

    @property
    def last_seen(self):
        try:
            return self.user_online.last_seen
        except ObjectDoesNotExist:
            return None

    @property
    def online_friends(self):
        return self.friends.with_online().filter(is_active=True, is_deleted=False, online=True)

    @property
    def geo(self):
        if not self.city:
            return "--"
        return "{country}/{region}/{city}".format(
            country=self.city.country.name if self.city.country else "--",
            region=self.city.region.name if self.city.region else "--",
            city=self.city.name,
        )

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class BlackList(GenericModelMixin, models.Model):
    BL_REASONS = (
        ("wanker", _("Wanker")),
        ("no_communication", _("Don't wont to communicate with the user")),
        ("just_so", _("Just So")),
        ("other", _("Other")),
    )
    creator = models.ForeignKey(
        User, verbose_name=_("Creator"), on_delete=models.CASCADE, related_name="creator_blacklists"
    )
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="user_blacklists")
    reason = models.CharField(_("Reason"), max_length=255, choices=BL_REASONS)
    reason_message = models.TextField(_("Reason Message"), default="")

    def __str__(self):
        return "{creator} - {user}".format(creator=self.creator, user=self.user)

    class Meta:
        unique_together = ("creator", "user")
        verbose_name = _("Black List")
        verbose_name_plural = _("Black List")


class UserLink(GenericModelMixin, models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="user_userlinks")
    link = models.CharField(_("Link"), max_length=255)
    description = models.TextField(_("Description"), null=True, blank=True)
    favicon = models.CharField(_("Favicon"), max_length=255, null=True, blank=True)

    def __str__(self):
        return "{user} - {link}".format(user=self.user, link=self.link)

    class Meta:
        verbose_name = _("User Link")
        verbose_name_plural = _("User Links")


class UserOnline(models.Model):
    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="user_online")
    last_seen = models.DateTimeField(verbose_name=_("Last seen"))

    @property
    def online(self):
        delta = timezone.now() - datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)
        return delta <= self.last_seen

    class Meta:
        verbose_name = _("User Online")
        verbose_name_plural = _("Users Online")
