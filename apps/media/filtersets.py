from django_filters import filters, filterset

from apps.generic.filtersets import ContentTypeFilter

from .models import Media, MediaFolder


class MediaFolderFilterSet(filterset.FilterSet):
    class Meta:
        model = MediaFolder
        fields = ("creator", "show_media")


class MediaFilterSet(filterset.FilterSet):
    hash_tag = filters.CharFilter(field_name="hash_tags", lookup_expr="icontains")
    content_type = ContentTypeFilter()

    class Meta:
        model = Media
        fields = ("object_id", "content_type", "media_type", "status", "hash_tag")
