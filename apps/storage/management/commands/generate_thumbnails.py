from django.core.management.base import BaseCommand
from tqdm import tqdm

from apps.storage.models import Image


class Command(BaseCommand):
    def handle(self, *args, **options):
        for image in tqdm(Image.objects.filter(is_deleted=False)):
            try:
                image.thumbnail_100x100.generate()
                image.thumbnail_500x500.generate()
                image.thumbnail_blur_100x100.generate()
                image.thumbnail_blur_500x500.generate()
            except FileNotFoundError:
                pass
