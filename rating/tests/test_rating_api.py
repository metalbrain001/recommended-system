"""
This module contains tests for the rating API.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Movie, Rating
from rating.serializer import RatingSerializer


RATING_URL = reverse("rating:rating-list")


def create_rating(user, movies, rating=5):
    """
    Create and return a new rating.
    """

    defaults = {
        "rating": rating,
    }
    rating = Rating.objects.create(user=user, movies=movies, **defaults)
    return rating


class publicRatingAPI(TestCase):
    """
    Test the public rating API.
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test that authentication is required.
        """

        res = self.client.get(RATING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class privateRatingAPI(TestCase):
    """
    Test the private rating API.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@example.com",
            "testpass123",
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ratings(self):
        """
        Test retrieving ratings.
        """

        movies = Movie.objects.create(
            user=self.user,
            title="Sample Movie",
            genre="Action",
            movieId=1,
        )

        create_rating(user=self.user, movies=movies)
        res = self.client.get(RATING_URL)
        ratings = Rating.objects.all().order_by("-rating")
        serializer = RatingSerializer(ratings, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_limited_to_user(self):
        """
        Test list of ratings in this method is
        limited to only the authenticated user.
        """
        user2 = get_user_model().objects.create_user(
            "other@example.com",
            "testpass123",
        )
        movies = Movie.objects.create(
            user=self.user,
            title="Sample Movie",
            genre="Action",
            movieId=1,
        )
        create_rating(user=user2, movies=movies)
        create_rating(user=self.user, movies=movies)
        res = self.client.get(RATING_URL)
        rating = Rating.objects.filter(user=self.user)
        serializer = RatingSerializer(rating, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)
