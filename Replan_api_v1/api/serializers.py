# api/serializers.py

from rest_framework import serializers
from .models import DssFiles


class LoadGraphSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = DssFiles
        fields = ('id', 'name', 'date_created', 'date_modified', 'path')
        read_only_fields = ('date_created', 'date_modified')