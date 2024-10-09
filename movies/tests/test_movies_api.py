"""
This module contains tests for the movies API.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Movie
from movies.serializer import MovieSerializer
from django.db import models

MOVIES_URL = reverse("movies:movie-list")


def create_movie(user, **params):
    """
    Create and return a sample movie.
    """
    # Get the maximum movieId currently in the database and add 1
    max_movie_id = Movie.objects.aggregate(max_id=models.Max("movieId"))["max_id"]
    new_movie_id = (max_movie_id or 0) + 1  # Default to 1 if no movies exist
    defaults = {
        "title": "Sample Movie",
        "genre": "Action",
        "movieId": new_movie_id,
    }
    defaults.update(params)
    movie = Movie.objects.create(user=user, **defaults)
    return movie


class publicMovieApiTests(TestCase):
    """
    Test the publicly available movies API.
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test that authentication is
        required for retrieving movies.
        """
        res = self.client.get(MOVIES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class privateMovieApiTests(TestCase):
    """
    Test the private movies API.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@example.com",
            "testpass123",
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_movies(self):
        """
        Test retrieving movies.
        """
        create_movie(user=self.user)
        create_movie(user=self.user)
        res = self.client.get(MOVIES_URL)
        movies = Movie.objects.all().order_by("-id")
        serializer = MovieSerializer(movies, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_limited_to_user(self):
        """
        Test list of movies returned are for
        the authenticated user.
        """
        user2 = get_user_model().objects.create_user(
            "other@example.com",
            "testpass123",
        )
        create_movie(user=user2)
        create_movie(user=self.user)
        res = self.client.get(MOVIES_URL)
        movies = Movie.objects.filter(user=self.user)
        serializer = MovieSerializer(movies, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)
