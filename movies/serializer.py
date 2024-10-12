"""
Serializer for movies app
"""

from rest_framework import serializers
from core.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for movie objects"""

    class Meta:
        model = Movie
        fields = ("id", "title", "genre", "movieId")
        read_only_fields = ("id",)
