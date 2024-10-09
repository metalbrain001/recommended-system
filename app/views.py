""" This file contains the views for the app. """

from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    """Home view for the app."""
    return render(request, "home.html")
