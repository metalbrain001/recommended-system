""" This file contains the views for the app. """

from django.shortcuts import render


def home(request):
    """Home view for the app."""
    return render(request, "home.html")
