from django.urls import path

from . import views

app_name = "listings"

urlpatterns = [
    path("listings", views.listings, name="index"),
    path("create", views.create, name="create"),
    path("<int:listing_id>", views.listing_detail, name="listing_detail"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("<int:listing_id>/close", views.close_auction, name="close_auction"),
]
