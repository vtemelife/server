from cities_light.models import City, Country, Region
from django.contrib import admin

admin.site.unregister(Country)
admin.site.unregister(Region)
admin.site.unregister(City)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code2", "code3", "continent", "tld", "phone", "geoname_id")
    search_fields = ("name", "name_ascii", "code2", "code3", "tld", "geoname_id")
    list_filter = ("continent",)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_filter = ("country__continent", "country")
    search_fields = ("name", "name_ascii", "geoname_id", "country__name", "country__alternate_names")
    list_display = ("name", "country", "geoname_id")
    autocomplete_fields = ("country",)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "country", "geoname_id", "timezone")
    search_fields = (
        "search_names",
        "geoname_id",
        "timezone",
        "region__name",
        "region__alternate_names",
        "country__name",
        "country__alternate_names",
    )
    list_filter = ("country__continent", "country", "timezone")
    autocomplete_fields = ("country", "region")
