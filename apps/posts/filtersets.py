from apps.generic.filtersets import BoolFilter, ContentTypeFilter
from django_filters import filters, filterset

from .models import Post


class PostFilterSet(filterset.FilterSet):
    hash_tag = filters.CharFilter(field_name="hash_tags", lookup_expr="icontains")
    content_type = ContentTypeFilter()
    is_whisper = BoolFilter()

    class Meta:
        model = Post
        fields = ("object_id", "content_type", "theme", "is_whisper", "status", "hash_tag")
