"""
This model contains tests for the tags API.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Movie, Tag
from tag.serializer import TagSerializer

TAGS_URL = reverse("movies:tag-list")


def create_user(email="user@example.com", password="testpass123"):
    """
    Create and return a sample user.
    """
    return get_user_model().objects.create_user(email=email, password=password)


class PublicTagsApiTests(TestCase):
    """
    Test the publicly and unauthenticated available tags API requests.
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test that login is required for retrieving tags.
        """

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """
    Test the authorized user tags API requests.
    """

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """
        Test retrieving tags.
        """

        Tag.objects.create(user=self.user, tag="Action")
        Tag.objects.create(user=self.user, tag="Comedy")

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by("-tag")
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """
        Test that tags returned are for the authenticated user.
        """

        user2 = create_user(email="user@example.com", password="testpass123")
        Tag.objects.create(user=user2, tag="Drama")
        tag = Tag.objects.create(user=self.user, tag="Action")

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["tag"], tag.tag)
        self.assertEqual(res.data[0]["user"], tag.user.id)
