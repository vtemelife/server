from django_filters import filterset

from .models import Shop


class ShopFilterSet(filterset.FilterSet):
    class Meta:
        model = Shop
        fields = ("name",)
