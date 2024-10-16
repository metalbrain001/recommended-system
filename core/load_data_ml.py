import pandas as pd
from core.models import Movie, Rating, Tag, Link
from django.contrib.auth import get_user_model
from django.db import transaction


def create_user(user_id):
    """
    Create a new user with a unique email based on user_id.
    """

    User = get_user_model()

    # Create a unique email by appending the user_id to the email string
    email = f"user_{user_id}@example.com"

    # Use get_or_create to avoid duplicate errors and ensure uniqueness
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'password': 'test1234'
        },  # Use a default password or generate dynamically
    )
    return user


class MovieLensDataLoader:
    """
    The MovieLensDataLoader class loads the
    MovieLens dataset files and inserts
    them into Django models.
    """

    def __init__(self, path=""):
        """
        Initialize path to the
        MovieLens dataset files.
        """
        self.path = path

    def load_data(self):
        """
        Loads MovieLens dataset files
        and inserts them into Django models.
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

    @transaction.atomic
    def load_movies(self, movies_df):
        """
        Insert movies data into the database.
        """

        # Skip movies if they already exist in the database
        existing_movies = set(Movie.objects.values_list("movieId", flat=True))
        movies_df = movies_df[~movies_df["movieId"].isin(existing_movies)]

        # Preload all users if you're associating users with movies
        user_map = {}
        movie_objects = []

        for index, row in movies_df.iterrows():
            if row["movieId"] not in user_map:
                user_map[row["movieId"]] = create_user(row["movieId"])

            movie = Movie(
                movieId=row["movieId"],
                title=row["title"],
                genre=row["genres"],
                user=user_map[row["movieId"]],
            )
            movie_objects.append(movie)
            index += 1

        Movie.objects.bulk_create(movie_objects, batch_size=5000)
        print(f"{len(movie_objects)} movies loaded into the database.")

    @transaction.atomic
    def load_ratings(self, ratings_df):
        """
        Insert ratings data into the database.
        """

        # Preload Movies and Users
        movie_map = {movie.movieId: movie for movie in Movie.objects.all()}
        user_map = {user.id: user for user in get_user_model().objects.all()}

        rating_objects = []
        for index, row in ratings_df.iterrows():
            if row["movieId"] in movie_map and row["userId"] in user_map:
                rating = Rating(
                    user=user_map[row["userId"]],
                    movies=Movie.objects.get(movieId=row["movieId"]),
                    rating=row["rating"],
                    timestamp=pd.to_datetime(row["timestamp"], unit="s"),
                )
                rating_objects.append(rating)
                index += 1

        Rating.objects.bulk_create(rating_objects, batch_size=5000)
        print(f"{len(rating_objects)} ratings loaded into the database.")

    @transaction.atomic
    def load_tags(self, tags_df):
        """
        Insert tags data into the database.
        """

        movie_map = {movie.movieId: movie for movie in Movie.objects.all()}
        user_map = {user.id: user for user in get_user_model().objects.all()}

        tag_objects = [
            Tag(
                user=user_map.get(row["userId"]),
                movie=movie_map.get(row["movieId"]),
                tag=row["tag"],
                timestamp=pd.to_datetime(row["timestamp"], unit="s"),
            )
            for index, row in tags_df.iterrows()
            if row["movieId"] in movie_map and row["userId"] in user_map
        ]

        Tag.objects.bulk_create(tag_objects, batch_size=5000)
        print(f"{len(tag_objects)} tags loaded into the database.")

    @transaction.atomic
    def load_links(self, links_df):
        """
        Insert links data into the database.
        """
        link_objects = [
            Link(
                movie_id=row["movieId"],
                imdbId=row["imdbId"],
                tmdbId=row["tmdbId"],
            )
            for index, row in links_df.iterrows()
        ]
        Link.objects.bulk_create(link_objects, batch_size=5000)
        print(f"{len(link_objects)} links loaded into the database.")
