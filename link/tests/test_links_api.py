"""
This module contains tests for the links API.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Movie, Link
from link.serializer import LinkSerializer


LINKS_URL = reverse("link:link-list")


def create_user(email="user@example.com", password="testpass123"):
    """
    Create and return a sample user.
    """

    return get_user_model().objects.create_user(email=email, password=password)


class PublicLinkApiTests(TestCase):
    """
    Test the publicly available links API.
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test that authentication is required for retrieving links.
        """

        res = self.client.get(LINKS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateLinkApiTests(TestCase):
    """
    Test the authorized user links API.
    """

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_links(self):
        """
        Test retrieving links.
        """

        Link.objects.create(
            user=self.user,
            movie="Movie1",
            linked_movie="Movie2",
            link_type="Similar",
        )
        Link.objects.create(
            user=self.user,
            movie="Movie3",
            linked_movie="Movie4",
            link_type="Similar",
        )

        res = self.client.get(LINKS_URL)

        links = Link.objects.all().order_by("-link_type")
        serializer = LinkSerializer(links, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_links_limited_to_user(self):
        """
        Test that links returned are for the authenticated user.
        """

        user2 = get_user_model().objects.create_user(
            "user@example.com",
            "testpass123",
        )

        link = Link.objects.create(
            user=self.user,
            movie="Movie7",
            linked_movie="Movie8",
            link_type="Similar",
        )
        Link.objects.create(
            user=user2,
            movie="Movie9",
            linked_movie="Movie10",
            link_type="Similar",
        )

        res = self.client.get(LINKS_URL)
        links = Link.objects.filter(user=self.user).order_by("-link_type")
        serializer = LinkSerializer(links, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_links_by_type(self):
        """
        Test retrieving links filtered by link_type.
        """

        Link.objects.create(
            user=self.user,
            movie=self.movie1,
            linked_movie=self.movie2,
            link_type="Sequel",
        )
        Link.objects.create(
            user=self.user,
            movie=self.movie3,
            linked_movie=self.movie4,
            link_type="Prequel",
        )

        res = self.client.get(LINKS_URL, {"link_type": "Sequel"})
        links = Link.objects.filter(user=self.user, link_type="Sequel")
        serializer = LinkSerializer(links, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

        res = self.client.get(LINKS_URL, {"link_type": "Prequel"})
        links = Link.objects.filter(user=self.user, link_type="Prequel")
        serializer = LinkSerializer(links, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

        res = self.client.get(LINKS_URL, {"link_type": "Similar"})
        links = Link.objects.filter(user=self.user, link_type="Similar")
        serializer = LinkSerializer(links, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recommendations(self):
        """
        Test retrieving recommended movies based on links.
        """

        Link.objects.create(
            user=self.user,
            movie=self.movie1,
            linked_movie=self.movie2,
            link_type="Sequel",
        )
        Link.objects.create(
            user=self.user,
            movie=self.movie2,
            linked_movie=self.movie3,
            link_type="Related",
        )

        res = self.client.get(reverse("link:recommendations"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data) > 0)
