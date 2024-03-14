from django.shortcuts import render
from models import Auction


# Create your views here.
def index(request):
    return render(
        request,
        "listings/index.html",
        {"listings": Auction.objects.filter(active=True)},
    )


def create(request):
    return render(request, "listings/create.html")


def listing(request, listing_id):
    listing_id = Auction.objects.get(pk=listing_id)
    return render(request, "listings/listing.html")


def watchlist(request):
    return render(request, "listings/watchlist.html")


def categories(request):
    return render(request, "listings/categories.html")
