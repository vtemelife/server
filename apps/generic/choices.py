from django.utils.translation import gettext_lazy as _


class ThemeChoices:
    THEME_SWING = "swing"
    THEME_BDSM = "bdsm"
    THEME_VIRT = "virt"
    THEME_LGBT = "lgbt"
    THEME_POLIAMORIA = "poliamoria"
    THEME_OTHER = "other"
    THEMES = (
        (THEME_SWING, _("Swing")),
        (THEME_BDSM, _("Bdsm")),
        (THEME_VIRT, _("Virt")),
        (THEME_LGBT, _("LGBT")),
        (THEME_POLIAMORIA, _("Poliamoria")),
        (THEME_OTHER, _("Other")),
    )


class ComminityTypeChoices:
    TYPE_OPEN = "open"
    TYPE_CLOSE = "close"
    TYPES = ((TYPE_OPEN, _("Open")), (TYPE_CLOSE, _("Close")))


class AccessChoices:
    ACCESS_NO_USERS = "no_users"
    ACCESS_ONLY_FRIENDS = "only_friends"
    ACCESS_ALL_USERS = "all_users"
    ACCESS = (
        (ACCESS_NO_USERS, _("No users")),
        (ACCESS_ONLY_FRIENDS, _("Only friends")),
        (ACCESS_ALL_USERS, _("All users")),
    )

    RELATIONSHIP_STATUS_OWNER = "owner"
    RELATIONSHIP_STATUS_FRIEND = "friend"
    RELATIONSHIP_STATUS_UNKNOWN = "unknown"
