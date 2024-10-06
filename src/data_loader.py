""" This module contains the MovieLensDataLoader class that loads the MovieLens dataset files. """

import pandas as pd


class MovieLensDataLoader:
    """The MovieLensDataLoader class loads the MovieLens dataset files."""

    def __init__(self, path=""):
        """
        Initialize path to the MovieLens dataset files.
        """
        self.path = path

    def load_data(self):
        """Loads MovieLens dataset files (movies, ratings, tags, links) from the given path
        Returns:
        movies (pd.DataFrame): Movies dataset
        ratings (pd.DataFrame): Ratings dataset
        tags (pd.DataFrame): Tags dataset
        links (pd.DataFrame): Links dataset
        """
        try:
            movies = pd.read_csv(f"{self.path}movies.csv")
            ratings = pd.read_csv(f"{self.path}ratings.csv")
            tags = pd.read_csv(f"{self.path}tags.csv")
            links = pd.read_csv(f"{self.path}links.csv")

            print("Files loaded successfully!")
            return movies, ratings, tags, links
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None, None, None, None
