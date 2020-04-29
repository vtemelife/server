from django.db.models import Q
from django_filters import filters


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ArrayInFilter(filters.BaseCSVFilter, filters.CharFilter):
    def filter(self, qs, value):
        if not value:
            return qs
        lookup = "%s__%s" % (self.field_name, "contains")
        q = Q()
        for val in value:
            q |= Q(**{lookup: [val]})
        return qs.filter(q).distinct()


class BoolFilter(filters.CharFilter):
    def filter(self, qs, value):
        if value == "false":
            return qs.filter(**{self.field_name: False})
        if value == "true":
            return qs.filter(**{self.field_name: True})
        return qs


class ContentTypeFilter(filters.CharFilter):
    def filter(self, qs, value):
        data = value.split(":")
        if len(data) != 2:
            return qs
        app_label, model = data
        return qs.filter(content_type__app_label=app_label, content_type__model=model)


class ParticipantFilter(filters.CharFilter):
    def filter(self, qs, value):
        if value == "true":
            qs = qs.filter(users=self.parent.request.user)
        return qs
