from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing

def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Listing.objects.all()
    })

def listing(request, listing_id):
    getListing = Listing.objects.get(id=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": getListing
    })

def category(request, category_str):
    getListingsInCategory = Listing.objects.filter(category=category_str)
    return render(request, "auctions/category.html", {
        "categorizedListings": getListingsInCategory,
        "category": category_str
    })

def watchlistAdd(request, listing_id):
    getListing = Listing.objects.get(id=listing_id)
    request.user.watching.add(getListing)
    request.user.save()
    return HttpResponseRedirect(reverse("index"))

def watchlist(request):
    print(request.user.watching)
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watching
    })

@login_required
def create(request):
    if request.method == "POST":
        newlisting = Listing(
            title = request.POST["title"],
            desc = request.POST["desc"],
            startingprice = request.POST["startingprice"],
            imageurl = request.POST["imageurl"]
        )
        newlisting.save()
        return render(request, "auctions/create.html", {
            "message": "Successfully Uploaded"
        })
    return render(request, "auctions/create.html")

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
