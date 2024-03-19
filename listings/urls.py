from django.urls import path

from . import views

app_name = 'listings'

urlpatterns = [
    path("listings", views.listings, name="listings"),
    path("create", views.create, name="create"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
]
