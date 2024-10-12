"""
Serializer for the rating app
"""

from rest_framework import serializers
from core.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    """Serializer for rating objects"""

    class Meta:
        model = Rating
        fields = ("id", "rating", "movies")
        read_only_fields = ("id",)
