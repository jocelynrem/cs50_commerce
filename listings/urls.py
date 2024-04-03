from django.urls import path

from . import views

app_name = "listings"

urlpatterns = [
    path("listings", views.listings, name="index"),
    path('create/', views.create_listing, name='create_listing'),
    path("<int:listing_id>", views.listing_detail, name="listing_detail"),
    path("watchlist", views.watchlist, name="watchlist"),
    path('toggle_watchlist/<int:listing_id>/', views.toggle_watchlist, name='toggle_watchlist'),
    path("<int:listing_id>/close", views.close_auction, name="close_auction"),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.listings_by_category, name='listings_by_category'),
]
