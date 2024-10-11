"""
Serializer for Link
"""

from rest_framework import serializers
from core.models import Link


class LinkSerializer(serializers.ModelSerializer):
    """
    Serializer for link objects
    """

    class Meta:
        model = Link
        fields = ("id", "link_type", "timestamp", "movie", "linked_movie", "user")
        read_only_fields = (
            "id",
            "timestamp",
            "user",
        )
