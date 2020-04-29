from apps.generic.filtersets import BoolFilter
from apps.users.models import User
from django_filters import filters, filterset


class IsRealWaitingFilter(filters.CharFilter):
    def filter(self, qs, value):
        if value == "true":
            return qs.filter(is_real=False).exclude(approver__isnull=True)
        return qs


class IsGuestFilter(filters.CharFilter):
    def filter(self, qs, value):
        if value == "true":
            return qs.filter(role=User.ROLE_GUEST)
        return qs


class IsBlackListFilter(filters.CharFilter):
    def filter(self, qs, value):
        if value == "true":
            return qs.filter(user_blacklists__isnull=False).distinct()
        return qs


class UserFilterSet(filterset.FilterSet):
    is_real = BoolFilter()
    is_ban = BoolFilter()
    is_real_waiting = IsRealWaitingFilter()
    is_guest = IsGuestFilter()
    is_black_list = IsBlackListFilter()

    class Meta:
        model = User
        fields = ("is_real", "is_real_waiting", "is_ban", "is_guest", "is_black_list")
