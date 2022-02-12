from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("addtowatchlist/<int:listing_id>", views.watchlistAdd, name="watchlistadd"),
    path("removefromwatchlist/<int:listing_id>", views.watchlistRemove, name="watchlistremove"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("createlisting", views.create, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("category/<str:category_str>", views.category, name="category"),
    path("bid", views.bid, name="bidding")
]
