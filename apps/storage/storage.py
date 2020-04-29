import logging

from django.core.files.storage import FileSystemStorage as BaseFileSystemStorage
from PIL import ExifTags, Image

logger = logging.getLogger("django")


class FileSystemStorage(BaseFileSystemStorage):
    def _fix_image_orientation(self, full_path):
        exif_keys = [k for k, v in ExifTags.TAGS.items() if v == "Orientation"]
        exif_key = (exif_keys and exif_keys[0]) or None
        if not exif_key:
            return

        try:
            img = Image.open(full_path)
        except IOError:
            # not image
            return

        try:
            getexif = getattr(img, "_getexif", None)
            if not getexif:
                # not support exif
                img.close()
                return

            exif_data = getexif()
            if not exif_data or exif_key not in exif_data:
                # no exif metadata
                img.close()
                return

            exif_orientation = exif_data[exif_key]
            if exif_orientation == 3:
                img = img.rotate(180, expand=True)
            elif exif_orientation == 6:
                img = img.rotate(270, expand=True)
            elif exif_orientation == 8:
                img = img.rotate(90, expand=True)
            img.save(full_path)

        except Exception as e:
            logger.exception(e)
        finally:
            img.close()

    def _save(self, name, content):
        filename = super()._save(name, content)
        full_path = self.path(filename)
        self._fix_image_orientation(full_path)
        return filename
