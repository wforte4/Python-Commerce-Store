from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid

def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Listing.objects.all()
    })

def listing(request, listing_id):
    getListing = Listing.objects.get(id=listing_id)
    getUserWatchList = request.user.watching.all()
    isOnWatchList = getListing in getUserWatchList
    allBids = Bid.objects.filter(on=getListing)
    print(allBids[0])
    return render(request, "auctions/listing.html", {
        "listing": getListing,
        "isOnWatchList": isOnWatchList
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
    return HttpResponseRedirect(reverse("watchlist"))

def watchlistRemove(request, listing_id):
    getListing = Listing.objects.get(id=listing_id)
    request.user.watching.remove(getListing)
    request.user.save()
    return HttpResponseRedirect(reverse("watchlist"))

@login_required
def watchlist(request):
    #Preview your watchlist to see your products
    print(request.user.watching.all())
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watching.all()
    })

@login_required
def bid(request):
    if request.method == "POST":
        getListing = Listing.objects.get(id=request.POST['listingid'])
        newbid = Bid(
            on = getListing,
            user = request.user,
            amount = request.POST["amount"]
        )
        newbid.save()
    return render(request, "auctions/index.html")

@login_required
def create(request):
    if request.method == "POST":

        #Create new listing
        newlisting = Listing(
            title = request.POST["title"],
            desc = request.POST["desc"],
            startingprice = request.POST["startingprice"],
            imageurl = request.POST["imageurl"],
            category = request.POST["category"]
        )
        #Save that listing
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
