from django.core.management.base import BaseCommand

from apps.storage.models import Image


class Command(BaseCommand):
    def handle(self, *args, **options):
        for image in Image.objects.filter(is_deleted=False):
            image.thumbnail_100x100.generate()
            image.thumbnail_500x500.generate()
            image.thumbnail_blur_100x100.generate()
            image.thumbnail_blur_500x500.generate()
