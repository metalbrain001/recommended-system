""" Module for content-based and collaborative filtering recommendation. """

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split


class RecommenderSystem:
    """Class for content and collaborative filtering recommendation."""

    def __init__(self, movies, ratings):
        """
        Initialize with movies and ratings DataFrames.
        """
        self.movies = movies
        self.ratings = ratings

    def content_based_filtering(self, movie_title, top_n=10):
        """
        Content-based filtering recommendation based on movie genres.
        Recommends movies similar to the given movie title.
        """
        # Use TF-IDF Vectorizer to calculate the similarity between genres
        tfidf = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf.fit_transform(self.movies["genres"])
        # Compute cosine similarity
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        # Find the index of the movie that matches the title
        idx = self.movies[self.movies["title"] == movie_title].index[0]
        # Get similarity scores for all movies
        sim_scores = list(enumerate(cosine_sim[idx]))
        # Sort movies by similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # Get the indices of the top-n most similar movies
        movie_indices = [i[0] for i in sim_scores[1 : top_n + 1]]
        # Return the top-n most similar movies
        return self.movies["title"].iloc[movie_indices]

    def collaborative_filtering(self):
        """
        Train a collaborative filtering model using the SVD algorithm from Surprise.
        """
        # Prepare data for Surprise library
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(
            self.ratings[["userId", "movieId", "rating"]], reader
        )
        # Split data into training and testing sets
        trainset, testset = train_test_split(data, test_size=0.25)
        # Use the SVD algorithm for collaborative filtering
        svd = SVD()
        svd.fit(trainset)
        # Test the model
        predictions = svd.test(testset)
        return svd, predictions

    def recommend_movies(self, user_id, svd_model, top_n=10):
        """
        Recommend top-n movies for a given user using collaborative filtering model (SVD).
        """
        # Get all movies
        all_movie_ids = self.ratings["movieId"].unique()
        # Predict ratings for all movies the user hasn't rated yet
        movies_not_rated = self.ratings[
            ~self.ratings["movieId"].isin(
                self.ratings[self.ratings["userId"] == user_id]["movieId"]
            )
        ]
        # Get predictions for unrated movies
        predictions = [
            (movie_id, svd_model.predict(user_id, movie_id).est)
            for movie_id in movies_not_rated["movieId"]
        ]
        # Get predictions for unrated movies
        predictions = [
            (movie_id, svd_model.predict(user_id, movie_id).est)
            for movie_id in all_movie_ids
        ]
        # Sort predictions by predicted rating
        predictions = sorted(predictions, key=lambda x: x[1], reverse=True)
        # Return the top-n recommended movies
        recommended_movie_ids = [pred[0] for pred in predictions[:top_n]]
        # Return movie titles
        return self.movies[self.movies["movieId"].isin(recommended_movie_ids)][
            "title"
        ]
