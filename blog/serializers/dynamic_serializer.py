from rest_framework import serializers


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """A ModelSerializer that takes a `fields` argument that controls
    which fields should be displayed."""

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' argument up to the superclass
        fields = kwargs.pop('fields', None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)