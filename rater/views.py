import json
from django.shortcuts import render
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt  # useful for post requests that come from js

from .models import User, Album, Rating

# loads index page
def index(request):
    return render(request, "rater/index.html")


# loads album page
def album(request):
    return render(request, "rater/album.html")


# allows user to log into their accounts
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "rater/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
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