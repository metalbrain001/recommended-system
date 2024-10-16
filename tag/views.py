"""
Tags views
"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from core.models import Tag
from tag import serializer


class TagViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    Manage tags in the database
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializer.TagSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """
        Return objects for the current
        authenticated user only
        """

        return (
            super()
            .get_queryset()
            .filter(user=self.request.user)
            .order_by("-tag")
        )

    def perform_create(self, serializer):
        """
        Create a new tag
        """
        if Tag.objects.filter(
            user=self.request.user, tag=serializer.validated_data["tag"]
        ).exists():
            raise serializer.ValidationError(
                "You have already created this tag."
            )
        serializer.save(user=self.request.user)
