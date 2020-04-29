"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD =
    'swpeople_server.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD =
    'swpeople_server.dashboard.CustomAppIndexDashboard'
"""

from admin_tools.dashboard import AppIndexDashboard, Dashboard, modules
from admin_tools.utils import get_admin_site_name
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for swpeople_server.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(
            modules.Group(
                _("Site management"),
                column=1,
                children=(
                    modules.ModelList(
                        _("Users"),
                        column=1,
                        models=(
                            "apps.users.models.*",
                            "django.contrib.auth.models.Group",
                            "apps.memberships.models.*",
                            "apps.management.models.*",
                        ),
                    ),
                    modules.ModelList(_("Emails"), column=1, models=("apps.mail.models.*",)),
                    modules.ModelList(_("Geo"), column=1, models=("cities_light.models.*",)),
                    modules.ModelList(_("Logs"), column=1, models=("apps.logs.models.*",)),
                    modules.ModelList(_("Files"), column=1, models=("apps.storage.models.*",)),
                ),
            )
        )

        self.children.append(
            modules.Group(
                _("Chat/Notification management"),
                column=1,
                children=(
                    modules.ModelList(_("News"), column=1, models=("apps.news.models.*",)),
                    modules.ModelList(_("Chat"), column=1, models=("apps.chat.models.*",)),
                    modules.ModelList(_("Notifications"), column=1, models=("apps.notifications.models.*",)),
                ),
            )
        )

        self.children.append(
            modules.Group(
                _("Content management"),
                column=1,
                children=(
                    modules.ModelList(_("Posts"), column=1, models=("apps.posts.models.*",)),
                    modules.ModelList(
                        _("Media"), column=1, models=("apps.media.models.MediaFolder", "apps.media.models.Media")
                    ),
                    modules.ModelList(_("Mobile Apps"), column=1, models=("apps.mobile.models.MobileVersion",)),
                    modules.ModelList(_("Comments"), column=1, models=("apps.comments.models.*",)),
                    modules.ModelList(_("Games"), column=1, models=("apps.games.models.*",)),
                ),
            )
        )

        self.children.append(
            modules.Group(
                _("Community management"),
                column=1,
                children=(
                    modules.ModelList(
                        _("Communities"),
                        column=1,
                        models=("apps.groups.models.*", "apps.clubs.models.*", "apps.events.models.*"),
                    ),
                    modules.ModelList(_("Shops"), column=1, models=("apps.shops.models.*",)),
                ),
            )
        )

        # append a link list module for "quick links"
        self.children.append(
            modules.LinkList(
                _("Quick links"),
                layout="inline",
                column=2,
                deletable=False,
                collapsible=False,
                children=[
                    [_("Return to site"), "/"],
                    [_("Change password"), reverse("%s:password_change" % site_name)],
                    [_("Log out"), reverse("%s:logout" % site_name)],
                ],
            )
        )

        # append a recent actions module
        self.children.append(modules.RecentActions(_("Recent Actions"), 5, column=2))


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for swpeople_server.
    """

    # we disable title because its redundant with the model list module
    title = ""

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(_("Recent Actions"), include_list=self.get_app_content_types(), limit=5),
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
