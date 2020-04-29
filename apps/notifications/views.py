from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response

from apps.chat.models import Chat
from apps.clubs.models import Club
from apps.events.models import Party
from apps.generic.permissions import IsAuthenticatedAndActive
from apps.groups.models import Group
from apps.media.models import Media
from apps.memberships.models import MembershipRequest
from apps.news.models import News
from apps.posts.models import Post
from apps.users.models import User


class CountersUserMixin:
    def get_u_unread_chats(self, user):
        return Chat.objects.user_chats(user).unread(user).count()

    def get_u_friends_requests_mine(self, user):
        return MembershipRequest.objects.filter(
            user_id=user.pk,
            is_deleted=False,
            content_type__app_label="users",
            content_type__model="user",
            status=MembershipRequest.STATUS_WAITING_MODERATION,
        ).count()

    def get_u_friends_requests(self, user):
        return MembershipRequest.objects.filter(
            object_id=user.pk,
            is_deleted=False,
            content_type__app_label="users",
            content_type__model="user",
            status=MembershipRequest.STATUS_WAITING_MODERATION,
        ).count()

    def get_u_clubs_requests(self, user):
        pks = Club.objects.filter(is_deleted=False, moderators=user).values_list("pk", flat=True)
        return MembershipRequest.objects.filter(
            object_id__in=pks,
            is_deleted=False,
            content_type__app_label="clubs",
            content_type__model="club",
            status=MembershipRequest.STATUS_WAITING_MODERATION,
        ).count()

    def get_u_groups_requests(self, user):
        pks = Group.objects.filter(is_deleted=False, moderators=user).values_list("pk", flat=True)
        return MembershipRequest.objects.filter(
            object_id__in=pks,
            is_deleted=False,
            content_type__app_label="groups",
            content_type__model="group",
            status=MembershipRequest.STATUS_WAITING_MODERATION,
        ).count()

    def get_u_events(self, user):
        return 0

    def get_u_cart(self, user):
        return 0

    def get_u_unread_news(self, user):
        return (
            News.objects.filter(is_deleted=False)
            .filter(Q(recipients__isnull=True) | Q(recipients=self.request.user))
            .filter(Q(theme__isnull=True) | Q(theme__in=self.request.user.relationship_themes))
            .published()
            .unread(user)
            .count()
        )


class CountersModeratorMixin:
    def get_m_unread_chats_moderators(self, user):
        if user.role != User.ROLE_MODERATOR:
            return 0
        return (
            Chat.objects.user_chats(user, is_moderator=True)
            .filter(chat_type=Chat.TYPE_CHAT_WITH_MODERATORS)
            .unread(user)
            .count()
        )

    def get_m_users_guest(self, user):
        if user.role != User.ROLE_MODERATOR:
            return 0
        return User.objects.filter(
            role=User.ROLE_GUEST, is_deleted=False, status=User.STATUS_WAITING_MODERATION
        ).count()

    def get_m_users_real(self, user):
        if user.role != User.ROLE_MODERATOR:
            return 0
        return User.objects.filter(is_real=False, is_deleted=False, status=User.STATUS_WAITING_MODERATION).count()

    def get_m_clubs_waiting_approve(self, user):
        if user.role != User.ROLE_MODERATOR:
            return 0
        return Club.objects.filter(is_deleted=False, status=Club.STATUS_WAITING_MODERATION).count()

    def get_m_parties_waiting_approve(self, user):
        if user.role != User.ROLE_MODERATOR:
            return 0
        return Party.objects.filter(is_deleted=False, status=Party.STATUS_WAITING_MODERATION).count()

    def get_m_posts_waiting_approve(self, user):
        if user.role != User.ROLE_MODERATOR:
            return 0
        return Post.objects.filter(is_deleted=False, status=Post.STATUS_WAITING_MODERATION).count()

    def get_m_media_waiting_approve(self, user):
        if user.role != User.ROLE_MODERATOR:
            return 0
        return Media.objects.filter(is_deleted=False, status=Media.STATUS_WAITING_MODERATION).count()

    def get_m_unpiblished_news(self, user):
        if user.role != User.ROLE_MODERATOR:
            return 0
        qs = News.objects.filter(is_deleted=False)
        return qs.not_published().count()


class CountersView(CountersUserMixin, CountersModeratorMixin, generics.GenericAPIView):
    permission_classes = (IsAuthenticatedAndActive,)

    def get(self, request, *args, **kwargs):
        user = request.user

        response = {
            "u_unread_chats": self.get_u_unread_chats(user),
            "u_friends_requests_mine": self.get_u_friends_requests_mine(user),
            "u_friends_requests": self.get_u_friends_requests(user),
            "u_clubs_requests": self.get_u_clubs_requests(user),
            "u_groups_requests": self.get_u_groups_requests(user),
            "u_events": self.get_u_events(user),
            "u_cart": self.get_u_cart(user),
            "u_unread_news": self.get_u_unread_news(user),
            "m_unread_chats_moderators": self.get_m_unread_chats_moderators(user),
            "m_users_guest": self.get_m_users_guest(user),
            "m_users_real": self.get_m_users_real(user),
            "m_clubs_waiting_approve": self.get_m_clubs_waiting_approve(user),
            "m_parties_waiting_approve": self.get_m_parties_waiting_approve(user),
            "m_posts_waiting_approve": self.get_m_posts_waiting_approve(user),
            "m_media_waiting_approve": self.get_m_media_waiting_approve(user),
            "m_unpiblished_news": self.get_m_unpiblished_news(user),
        }
        response["u_notifications"] = (
            response["u_unread_chats"]
            + response["u_friends_requests"]
            + response["u_clubs_requests"]
            + response["u_groups_requests"]
            + response["u_events"]
            + response["u_unread_news"]
        )
        response["m_notifications"] = (
            response["m_unread_chats_moderators"]
            + response["m_clubs_waiting_approve"]
            + response["m_parties_waiting_approve"]
            + response["m_posts_waiting_approve"]
            + response["m_media_waiting_approve"]
            + response["m_unpiblished_news"]
        )
        response["m_unread_chats"] = response["m_unread_chats_moderators"]
        response["m_users"] = 0
        return Response(response)
