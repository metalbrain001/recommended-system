"""
Link Views
"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from core.models import Link
from link import serializer


class LinkViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    Manage links in the database
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Link.objects.all()
    serializer_class = serializer.LinkSerializer

    def get_queryset(self):
        """
        Return objects for the current
        authenticated user only
        """

        return (
            super()
            .get_queryset()
            .filter(user=self.request.user)
            .order_by("-timestamp")
        )

    def perform_create(self, serializer):
        """
        Create a new link
        """

        if Link.objects.filter(
            user=self.request.user,
            movie=serializer.validated_data["movie"],
            linked_movie=serializer.validated_data["linked_movie"],
            link_type=serializer.validated_data["link_type"],
        ).exists():
            raise serializer.ValidationError(
                "You have already created this link."
            )
        serializer.save(user=self.request.user)
