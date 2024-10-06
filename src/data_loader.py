"""
This module contains the MovieLensDataLoader
class that loads the MovieLens dataset files.
"""

import pandas as pd


class MovieLensDataLoader:
    """The MovieLensDataLoader class loads the MovieLens dataset files."""

    def __init__(self, path=""):
        """
        Initialize path to the MovieLens dataset files.
        """
        self.path = path

    def load_data(self):
        """Loads MovieLens dataset files
        (movies, ratings, tags, links)
        from the given path
        Returns:
        movies (pd.DataFrame): Movies dataset
        ratings (pd.DataFrame): Ratings dataset
        tags (pd.DataFrame): Tags dataset
        links (pd.DataFrame): Links dataset
        """
        try:
            MOVIES = pd.read_csv(f"{self.path}movies.csv")
            RATINGS = pd.read_csv(f"{self.path}ratings.csv")
            TAGS = pd.read_csv(f"{self.path}tags.csv")
            LINKS = pd.read_csv(f"{self.path}links.csv")

            print("Files loaded successfully!")
            return MOVIES, RATINGS, TAGS, LINKS
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None, None, None, None
