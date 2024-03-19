from django.urls import path

from . import views

urlpatterns = [
    path("listings", views.listings, name="listings"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
]
