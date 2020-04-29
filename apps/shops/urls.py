from django.urls import path

from .views import ShopCreateView, ShopDeleteView, ShopListView, ShopRetrieveView, ShopUpdateView

app_name = "apps.shops"

urlpatterns = [
    path("", ShopListView.as_view(), name="shop-list"),
    path("create/", ShopCreateView.as_view(), name="shop-create"),
    path("<uuid:pk>/", ShopRetrieveView.as_view(), name="shop-retrieve"),
    path("<uuid:pk>/update/", ShopUpdateView.as_view(), name="shop-update"),
    path("<uuid:pk>/delete/", ShopDeleteView.as_view(), name="shop-delete"),
]
