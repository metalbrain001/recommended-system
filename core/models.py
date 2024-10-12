"""
Database modal
"""

from decimal import Decimal
from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """
    Manager User.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create, save and return a new user.
        """
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password):
        """
        Create and return a new superuser.
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User in the System
    """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Movie(models.Model):
    """
    Movies for the user
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movieId = models.IntegerField(unique=True)
    imdbId = models.CharField(max_length=255, null=True, blank=True)
    tmdbId = models.DecimalField(
        max_digits=10, decimal_places=1, null=True, blank=True
    )
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Movie"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Rating(models.Model):
    """
    Ratings for the user
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movies = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal("1.0")),
            MaxValueValidator(Decimal("5.0")),
        ],
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "rating")
        verbose_name_plural = "Ratings"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.movies.title} - {self.rating}"


class Tag(models.Model):
    """
    Tags for filtering movies.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    tag = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie", "tag")
        ordering = ["-timestamp"]

    def __str__(self):
        return f'{self.user} tagged {self.movie} with "{self.tag}"'

    @classmethod
    def filter_movies_by_tag(cls, tag_name):
        """
        Return all movies that have been tagged
        with the specified tag.
        """

        return Movie.objects.filter(tag__tag=tag_name)


class Link(models.Model):
    """
    Links between movies.
    """

    SEQUEL = "Sequel"
    PREQUEL = "Prequel"
    REMAKE = "Remake"
    RELATED = "Related"

    LINK_TYPES = [
        (SEQUEL, "Sequel"),
        (PREQUEL, "Prequel"),
        (REMAKE, "Remake"),
        (RELATED, "Related"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    linked_movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="linked_movie"
    )
    link_type = models.CharField(
        max_length=20, choices=LINK_TYPES, default=RELATED
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie", "linked_movie")
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user} linked {self.movie}({self.link_type}) with {self.linked_movie}"

    @classmethod
    def get_linked_movies(self):
        """
        Returns a queryset of all movies linked to this movie.
        """

        return Link.objects.filter(movie=self.movie)

    @classmethod
    def get_links_by_type(cls, link_type):
        """
        Filter linked movies by a specific type of link.
        """

        return cls.objects.filter(link_type=link_type)
