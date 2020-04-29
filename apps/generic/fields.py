import json

import six
from django.contrib.contenttypes.models import ContentType
from rest_framework.fields import CharField, ChoiceField, Field


class ChoiceDisplayField(ChoiceField):
    def __init__(self, *args, **kwargs):
        super(ChoiceDisplayField, self).__init__(*args, **kwargs)
        self.choice_strings_to_display = {six.text_type(key): value for key, value in self.choices.items()}

    def to_representation(self, value):
        if value is None:
            return value
        if not isinstance(value, list):
            return {
                "value": self.choice_strings_to_values.get(six.text_type(value), value),
                "display": self.choice_strings_to_display.get(six.text_type(value), value),
            }
        else:
            return [
                {
                    "value": self.choice_strings_to_values.get(six.text_type(item), item),
                    "display": self.choice_strings_to_display.get(six.text_type(item), item),
                }
                for item in value
            ]


class ContentTypeField(CharField):
    def to_representation(self, value):
        return "%s:%s" % (value.app_label, value.model)

    def to_internal_value(sefl, data):
        if data:
            app_label, model = data.split(":")
            data = ContentType.objects.get(app_label=app_label, model=model)
        return data


class JSONSerializerField(Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        json_data = {}
        try:
            json_data = json.loads(data)
        except ValueError:
            pass
        finally:
            return json_data


class HashTagsField(CharField):
    def to_representation(self, value):
        if not value:
            return []
        return [hash_tag.strip() for hash_tag in value.strip().split("#") if hash_tag]

    def to_internal_value(self, data):
        return data
