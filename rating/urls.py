"""
Rating app mapping URL configuration.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rating import views

router = DefaultRouter()
router.register("ratings", views.RatingViewSet)

app_name = "rating"

urlpatterns = [
    path("", include(router.urls)),
]
