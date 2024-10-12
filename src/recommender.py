""" Module for content-based and collaborative filtering recommendation. """

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split


class RecommenderSystem:
    """
    Class for content and collaborative
    filtering recommendation.
    """

    def __init__(self, MOVIES, RATINGS):
        """
        Initialize with movies and ratings DataFrames.
        """
        self.movies = MOVIES
        self.ratings = RATINGS

    def content_based_filtering(self, MOVIE_TITLE, TOP_N=10):
        """
        Content-based filtering
        recommendation based on movie genres.
        Recommends movies similar to the given movie title.
        """
        # Use TF-IDF Vectorizer to calculate the similarity between genres
        TFIDF = TfidfVectorizer(stop_words="english")
        TFIDF_MATRIX = TFIDF.fit_transform(self.movies["genres"])
        # Compute cosine similarity
        COSINE_SIM = cosine_similarity(TFIDF_MATRIX, TFIDF_MATRIX)
        # Find the index of the movie that matches the title
        IDX = self.movies[self.movies["title"] == MOVIE_TITLE].index[0]
        # Get similarity scores for all movies
        SIM_SCORES = list(enumerate(COSINE_SIM[IDX]))
        # Sort movies by similarity scores
        SIM_SCORES = sorted(SIM_SCORES, key=lambda x: x[1], reverse=True)
        # fmt: off
        MOVIE_INDICIES = [i[0] for i in SIM_SCORES[1: TOP_N + 1]]
        # fmt: on
        # Return the top-n most similar movies
        return self.movies["title"].iloc[MOVIE_INDICIES]

    def collaborative_filtering(self):
        """
        Train a collaborative filtering model
        using the SVD algorithm from Surprise.
        """

        # Prepare data for Surprise library
        READER = Reader(rating_scale=(1, 5))
        DATA = Dataset.load_from_df(
            self.ratings[["userId", "movieId", "rating"]], READER
        )
        # Split data into training and testing sets
        TRAINSET, TESTSET = train_test_split(DATA, TEST_SIZE=0.25)
        # Use the SVD algorithm for collaborative filtering
        svd = SVD()
        svd.fit(TRAINSET)
        # Test the model
        predictions = svd.test(TESTSET)
        return svd, predictions

    def recommend_movies(self, user_id, svd_model, top_n=10):
        """
        Recommend top-n movies for a given user
        using collaborative filtering model (SVD).
        """

        # Get all movies
        ALL_MOVIES_ID = self.ratings["movieId"].unique()
        # Predict ratings for all movies the user hasn't rated yet
        MOVIES_NOT_RATED = self.ratings[
            ~self.ratings["movieId"].isin(
                self.ratings[self.ratings["userId"] == user_id]["movieId"]
            )
        ]
        # Get predictions for unrated movies
        PREDICTIONS = [
            (MOVIE_ID, svd_model.predict(user_id, MOVIE_ID).est)
            for MOVIE_ID in MOVIES_NOT_RATED["movieId"]
        ]
        # Get predictions for all movies
        PREDICTIONS = [
            (movie_id, svd_model.predict(user_id, movie_id).est)
            for movie_id in ALL_MOVIES_ID
        ]
        # Sort predictions by predicted rating
        PREDICTIONS = sorted(PREDICTIONS, key=lambda x: x[1], reverse=True)
        # Return the top-n recommended movies
        RECOMMENDED_MOVIES_ID = [pred[0] for pred in PREDICTIONS[:top_n]]
        # Return movie titles
        return self.movies[self.movies["movieId"].isin(RECOMMENDED_MOVIES_ID)][
            "title"
        ]
