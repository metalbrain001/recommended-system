"""
Test for models
"""

from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Movie, Rating
from core import models


def create_user(email="user@example.com", password="testpass123"):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["TEST2@Example.com", "TEST2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "test123",
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_movies(self):
        """Test creating a movie is successful."""
        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="test123",
        )
        movie = models.Movie.objects.create(
            user=user, title="Inception", genre="Action, Sci-Fi", movieId=1
        )
        # Check that the movie was created successfully
        self.assertEqual(movie.title, "Inception")
        self.assertEqual(movie.genre, "Action, Sci-Fi")
        self.assertEqual(movie.movieId, 1)

        # String representation should be the movie title
        self.assertEqual(str(movie), movie.title)

    def test_create_ratings(self):
        """Test creating a rating is successful."""
        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="test123",
        )
        movie = Movie.objects.create(
            user=user, title="Inception", genre="Action, Sci-Fi", movieId=1
        )
        rating = Rating.objects.create(
            user=user,
            rating=Decimal("4.5"),
            movies=movie,
        )
        self.assertEqual(
            str(rating), f"{rating.user} - {rating.movies} - {rating.rating}"
        )
