import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # useful for post requests that come from js

# loads index page
def index(request):
    return render(request, "rater/index.html")

# loads album page
def album(request):
    return render(request, "rater/album.html")
