"""
Views for the rating app.
"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from core.models import Rating
from rating import serializer
from rest_framework import filters


class RatingPagination(PageNumberPagination):
    page_size = 10


class RatingViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    Manage ratings in the database.
    """

    pagination_class = RatingPagination

    serializer_class = serializer.RatingSerializer
    queryset = Rating.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["movie__title"]
    ordering_fields = ["created_at", "rating"]

    def get_queryset(self):
        """
        Return objects for the current authenticated user only.
        """
        return self.queryset.filter(user=self.request.user).order_by("-rating")

    def perform_create(self, serializer):
        """Create a new rating."""
        if Rating.objects.filter(
            movie=serializer.validated_data["movies"]
        ).exists():
            raise serializer.ValidationError("You have already rated this movie.")
        serializer.save(user=self.request.user)
