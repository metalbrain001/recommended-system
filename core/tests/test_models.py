"""
Test for models
"""

from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Movie, Rating
from core import models


def create_user(email="user@example.com", password="testpass123"):
    """
    Create and return a new user.
    """

    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    """
    Test models.
    """

    def test_create_user_with_email_successful(self):
        """
        Test creating a user with an email is successful
        """

        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test email is normalized for new users.
        """

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
        """
        Test that creating a user without email raises a ValueError.
        """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        """
        Test creating a superuser.
        """

        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "test123",
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_movies(self):
        """
        Test creating a movie is successful.
        """

        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="test123",
        )
        movie = models.Movie.objects.create(
            user=user,
            title="Inception",
            genre="Action, Sci-Fi",
            movieId=1,
            imdbId="1375666",
            tmdbId=27205.0,
        )
        # Check that the movie was created successfully
        self.assertEqual(movie.title, "Inception")
        self.assertEqual(movie.genre, "Action, Sci-Fi")
        self.assertEqual(movie.movieId, 1)
        self.assertEqual(movie.imdbId, "1375666")
        self.assertEqual(movie.tmdbId, 27205.0)

        # String representation should be the movie title
        self.assertEqual(str(movie), movie.title)

    def test_create_ratings(self):
        """
        Test creating a rating is successful.
        """

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

    def test_create_tag(self):
        """
        Test creating a tag is successful.
        """

        user = create_user()
        movie = models.Movie.objects.create(
            user=user, title="Sample Movie", genre="Action", movieId=123
        )
        tag = models.Tag.objects.create(user=user, movie=movie, tag="Tag1")
        self.assertEqual(str(tag), f'{user} tagged {movie} with "Tag1"')

    def test_filter_movies_by_tag(self):
        """
        Test filtering movies by a specific tag.
        """

        user = create_user()
        movie1 = models.Movie.objects.create(
            user=user, movieId=124, title="Sample Movie 1", genre="Action"
        )
        movie2 = models.Movie.objects.create(
            user=user, movieId=125, title="Sample Movie 2", genre="Comedy"
        )

        # Tagging movies
        models.Tag.objects.create(user=user, movie=movie1, tag="Action")
        models.Tag.objects.create(user=user, movie=movie2, tag="Comedy")

        # Filtering movies by tag
        action_movies = models.Tag.filter_movies_by_tag("Action")

        self.assertIn(movie1, action_movies)
        self.assertNotIn(movie2, action_movies)

    def test_create_links(self):
        """
        Test creating links between movies.
        """

        user = create_user()
        movie1 = models.Movie.objects.create(
            user=user, movieId=126, title="Sample Movie 1", genre="Action"
        )
        movie2 = models.Movie.objects.create(
            user=user, movieId=127, title="Sample Movie 2", genre="Comedy"
        )

        # Creating links between movies with link types
        link = models.Link.objects.create(
            user=user,
            movie=movie1,
            linked_movie=movie2,
            link_type=models.Link.SEQUEL,
        )

        self.assertEqual(link.link_type, models.Link.SEQUEL)
        self.assertEqual(
            str(link), f"{user} linked {movie1} (Sequel) with {movie2}"
        )

        # Test filtering by link type
        sequels = models.Link.get_links_by_type(models.Link.SEQUEL)
        self.assertIn(link, sequels)
