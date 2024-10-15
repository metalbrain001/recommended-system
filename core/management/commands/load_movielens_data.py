from django.core.management.base import BaseCommand
from core.load_data_ml import MovieLensDataLoader


class Command(BaseCommand):
    """
    Django command to load the MovieLens dataset into the database
    """

    def handle(self, *args, **options):
        self.stdout.write("Loading MovieLens data into the database...")

        # Initialize the data loader with the path to your dataset
        loader = MovieLensDataLoader(path="ml-32m/")

        # Load the data into the database
        loader.load_data()

        self.stdout.write(
            self.style.SUCCESS("MovieLens data loaded successfully!")
        )
