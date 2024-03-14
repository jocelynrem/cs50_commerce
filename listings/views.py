from django.shortcuts import render
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):
    return render(request, "listings/index.html")

@login_required
def create(request):
    return render(request, "listings/create.html")


def listing(request, listing_id):
    listing_id = Auction.objects.get(pk=listing_id)
    return render(request, "listings/listing.html")

@login_required
def watchlist(request):
    return render(request, "listings/watchlist.html")


def categories(request):
    return render(request, "listings/categories.html")
