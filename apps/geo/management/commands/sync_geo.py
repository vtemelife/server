# flake8: noqa
from cities_light.models import City, Country, Region
from django.core.management.base import BaseCommand
from django.db import models
from django.template.defaultfilters import slugify

from apps.clubs.models import Club
from apps.users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        for old, new in (
            ("Moscow", "Moscow Oblast"),
            ("Leningradskya oblast", "Leningradskaya Oblast'"),
            ("St.-Petersburg", "Leningradskaya Oblast'"),
        ):
            region = Region.objects.filter(name=old).first()
            if region:
                new_region = Region.objects.get(name=new)
                City.objects.filter(region=region).update(region=new_region)
                region.delete()

        for old, new in (("Sankt-Peterburg", "Saint Petersburg"),):
            city = City.objects.filter(name=old).first()
            if city:
                new_city = City.objects.get(name=new)
                User.objects.filter(city=city).update(city=new_city)
                Club.objects.filter(city=city).update(city=new_city)
                city.delete()

        country_russia = Country.objects.get(name="Russia")
        region_crimea = Region.objects.get(name="Republic of Crimea")
        region_crimea.country = country_russia
        region_crimea.display_name = "Republic of Crimea, Russia"
        region_crimea.save(update_fields=("country", "display_name"))
        City.objects.filter(region=region_crimea).update(country=country_russia)

        City.objects.filter(alternate_names="St. Petersburg;St.-Petersburg;СПб").update(
            alternate_names="Санкт Петербург"
        )
        Country.objects.filter(alternate_names="Russian Federation;Российская Федерация").update(
            alternate_names="Russian Federation;Российская Федерация;Россия"
        )
