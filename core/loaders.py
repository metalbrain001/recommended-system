"""
This module contains the MovieLensDataLoader
class that loads the MovieLens dataset files and
inserts them into the Django models.
"""

import pandas as pd
from core.models import Movie, Rating, Tag, Link
from django.utils.dateparse import parse_datetime
from django.contrib.auth import get_user_model


def create_user(user_id):
    """
    Create a new user with the given user_id.
    """

    User = get_user_model()
    user = User.objects.create_user(
        email=f"user_{user_id}@example.com",  # Unique email based on user_id
        password="password",
    )
    return user


class MovieLensDataLoader:
    """
    The MovieLensDataLoader class loads
    the MovieLens dataset files.
    """

    def __init__(self, path=""):
        """
        Initialize path to the MovieLens dataset files.
        """
        self.path = path

    def load_data(self):
        """
        Loads MovieLens dataset files and
        inserts them into Django models.
        """

        try:
            movies_df = pd.read_csv(f"{self.path}movies.csv")
            ratings_df = pd.read_csv(f"{self.path}ratings.csv")
            tags_df = pd.read_csv(f"{self.path}tags.csv")
            links_df = pd.read_csv(f"{self.path}links.csv")

            print("Files loaded successfully!")

            # Insert movies into the database
            self.load_movies(movies_df)
            self.load_ratings(ratings_df)
            self.load_tags(tags_df)
            self.load_links(links_df)

        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None

    def load_movies(self, movies_df):
        """
        Insert movies data into the database.
        """

        movie_objects = []
        for index, row in movies_df.iterrows():
            user = create_user(row["movieId"])
            movie = Movie.objects.create(
                movieId=row["movieId"],
                title=row["title"],
                genre=row["genres"],
                user=user,
            )
            movie_objects.append(movie)
            index += 1
        Movie.objects.bulk_create(movie_objects, batch_size=1000)
        print(f"{len(movie_objects)} movies loaded into the database.")

    def load_ratings(self, ratings_df):
        """
        Insert ratings data into the database.
        """

        rating_objects = []
        for index, row in ratings_df.iterrows():
            movie = Movie.objects.get(movieId=row["movieId"])
            user = get_user_model().objects.get(id=row["userId"])
            timestamp = parse_datetime(row["timestamp"])
            rating = Rating(
                user=user,
                movie=movie,
                rating=row["rating"],
                timestamp=timestamp,
            )
            rating_objects.append(rating)
            index += 1

        Rating.objects.bulk_create(rating_objects, batch_size=1000)
        print(f"{len(rating_objects)} ratings loaded into the database.")

    def load_tags(self, tags_df):
        """
        Insert tags data into the database.
        """

        tag_objects = []
        for index, row in tags_df.iterrows():
            user = get_user_model().objects.get(id=row["userId"])
            movie = Movie.objects.get(movieId=row["movieId"])
            tag = Tag(
                user=user,
                movie_id=movie,
                tag=tag,
                timestamp=pd.to_datetime(row["timestamp"], unit="s"),
            )
            tag_objects.append(tag)
            index += 1

        Tag.objects.bulk_create(tag_objects, batch_size=1000)
        print(f"{len(tag_objects)} tags loaded into the database.")

    def load_links(self, links_df):
        """
        Insert links data into the database.
        """

        link_objects = []
        for index, row in links_df.iterrows():
            movie = Movie.objects.get(movieId=row["movieId"])
            link = Link(
                movie_id=movie,
                imdbId=row["imdbId"],
                tmdbId=row["tmdbId"],
            )

        Link.objects.bulk_create(link_objects, batch_size=1000)
        print(f"{len(link_objects)} links loaded into the database.")
