import json
from django.shortcuts import render
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from datetime import datetime  # used when saving albums
from django.views.decorators.csrf import csrf_exempt  # useful for post requests that come from js

from .models import User, Album, Rating

# loads index page
def index(request):
    return render(request, "rater/index.html")


# loads album page
def album(request, album_id):
    # checks if album has been saved by the user
    profile = User.objects.get(username=request.user.username)
    in_database = profile.saved_albums.filter(pk=album_id).exists()

    # gets rating for template rendering
    album = Album.objects.get(id=album_id)
    try:
        ratingObj = Rating.objects.get(user=profile, album=album)
        rating = ratingObj.rating
    except Rating.DoesNotExist:
        rating = 0

    if rating != 0:
        empty = 5 - rating
    else:
        empty = 0

    return render(request, "rater/album.html", {
        "in_database": in_database,
        "rating": range(rating),
        "empty": range(empty)
    })


# saves album and rating to database
@csrf_exempt
def save_album(request):
    # gets info from json data
    data = json.loads(request.body)
    albumID = data.get("album")
    rating = data.get("rating")

    # checks if the album is in database and adds it if it isn't
    if Album.objects.filter(id=albumID).exists():
        album = Album.objects.get(id=albumID)
    else:
        album = Album(id=albumID)
        album.save()

    # adds rating to database
    if request.user.is_authenticated:
        user = request.user._wrapped
        rating = Rating(
            user = user,
            album = album,
            datetime = datetime.now(),
            rating = rating
        )
        rating.save()

    # adds album to user's saved_albums
    request.user.saved_albums.add(album)

    return JsonResponse({"message": "Album saved successfully."}, status=201) 


# unsaves album from user's db and rating from database
@csrf_exempt
def unsave_album(request):
    # gets info from json data
    data = json.loads(request.body)
    albumID = data.get("album")

    # removes album from user's saved albums
    album = Album.objects.get(id=albumID)
    request.user.saved_albums.remove(album)

    # removes rating from db
    rating = Rating.objects.get(user=request.user, album=album)
    rating.delete()

    return JsonResponse({"message": "Album unsaved successfully."}, status=201) 


# allows user to log into their accounts
def login_view(request):
    if request.method == "POST":

        # attempts to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # checks if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "rater/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "rater/login.html")


# allows users to log out of their accounts
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# allows user to register
def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        email = None

        # ensures password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "rater/register.html", {
                "message": "Passwords must match."
            })

        # attempts to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "rater/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "rater/register.html")