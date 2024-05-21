import json
from django.shortcuts import render
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db.models import Sum  # to sum a user's ratings
from django.core.paginator import Paginator  # to paginate through ratings
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
    try:
        album = Album.objects.get(id=album_id)
        ratingObj = Rating.objects.get(user=profile, album=album)
        rating = ratingObj.rating
        review = ratingObj.review
    except (Rating.DoesNotExist, Album.DoesNotExist):
        rating = 0
        review = "Write your review here!"

    if rating != 0:
        empty = 5 - rating
    else:
        empty = 0

    return render(request, "rater/album.html", {
        "in_database": in_database,
        "rating": range(rating),
        "empty": range(empty),
        "review": review
    })


# saves album and rating to database
@csrf_exempt
def save_album(request):
    # gets info from json data
    data = json.loads(request.body)
    albumID = data.get("albumID")
    rating = data.get("rating")
    review = data.get("review")

    # checks if the album is in database and adds it if it isn't
    if Album.objects.filter(id=albumID).exists():
        album = Album.objects.get(id=albumID)
    else:
        album = Album(
            id = albumID,
            name = data.get("albumName"),
            img = data.get("albumImg"),
            release = data.get("albumRelease")
        )
        album.save()

    # adds rating to database
    if request.user.is_authenticated:
        user = request.user._wrapped
        rating = Rating(
            user = user,
            album = album,
            datetime = datetime.now(),
            rating = rating,
            review = review
        )
        rating.save()

    # adds rating to user's ratings
    request.user.ratings.add(rating)

    # adds album to user's saved albums
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


# loads library page
def library(request):
    # orders saved albums and adds stars 
    by_new = request.user.ratings.all().order_by('-datetime')  # from newest rated
    by_old = request.user.ratings.all().order_by('datetime')  # from oldest rated
    by_high = request.user.ratings.all().order_by('-rating')  # from highest rated
    by_low = request.user.ratings.all().order_by('rating')  # from lowest rated
    
    # renders library page
    return render(request, "rater/library.html", {
        'by_new': by_new,
        'by_old': by_old,
        'by_high': by_high,
        'by_low': by_low
    })


# loads recent page
def recent(request):
    # creates a paginator object with all posts ordered from most recentß
    p = Paginator(Rating.objects.all().order_by('-datetime'), 10)

    # gets the correct page
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    # get user's liked ratings
    liked_ratings = []
    if request.user.is_authenticated:
        liked_ratings = request.user.liked_ratings.all()

    return render(request, "rater/recent.html", {
        "page_obj": page_obj,
        "liked_ratings": liked_ratings
    })

# likes a rating update
@csrf_exempt
def like_rating(request):
    # gets data from js 
    data = json.loads(request.body)
    ratingID = data.get("ratingID")
    print(ratingID)
    
    try:
        rating = Rating.objects.get(id=ratingID)
    except:
        return JsonResponse({"error": "Post does not exist."}, status=400)

    rating.likes = rating.likes + 1
    rating.save()

    # saves post to user's liked_posts
    request.user.liked_ratings.add(rating)

    return JsonResponse({"message": "Rating liked successfully.", "likes": rating.likes}, status=201)


# unlikes a rating update
@csrf_exempt
def unlike_rating(request):
    # gets data from js 
    data = json.loads(request.body)
    ratingID = data.get("ratingID")
    
    try:
        rating = Rating.objects.get(id=ratingID)
    except:
        return JsonResponse({"error": "Post does not exist."}, status=400)

    rating.likes = rating.likes - 1
    rating.save()

    # removes post to user's liked_posts
    request.user.liked_ratings.remove(rating)

    return JsonResponse({"message": "Rating unliked successfully.", "likes": rating.likes}, status=201)


# loads profile page for any user
def profile(request, username):
    # get the profile and relevant info
    profile = User.objects.get(username=username)
    ratings = Rating.objects.filter(user=profile).order_by('-datetime')
    rating_count = ratings.count()

    # gets user's average rating
    total_ratings = Rating.objects.filter(user=profile).aggregate(Sum('rating'))  # this returns a dictionary
    average = round(total_ratings['rating__sum'] / rating_count, 2)  # round off to two decimals

    # renders the template with said info
    return render(request, "rater/profile.html", {
        "profile": profile,
        "ratings": ratings,
        "liked_ratings": request.user.liked_ratings.all(),
        "rating_count": rating_count,
        "average": average
    })


# REGISTER LOGIN AND LOGOUT FUNCTIONS

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