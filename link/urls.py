"""
Link Urls Mappings
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from link import views

router = DefaultRouter()
router.register("links", views.LinkViewSet)

app_name = "link"

urlpatterns = [
    path("", include(router.urls)),
]
