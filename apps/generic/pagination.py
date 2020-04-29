from rest_framework.pagination import LimitOffsetPagination


class ReverseLimitOffsetPagination(LimitOffsetPagination):
    def get_offset(self, request):
        offset = super().get_offset(request)
        limit = self.get_limit(request)
        count = self.count
        return count - (limit + offset) if count - (limit + offset) >= 0 else 0
