from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


from auctions.models import Listing, User, Comment


# Create your views here.
def listings(request):
    return render(request, "listings/index.html")


@login_required
def create(request):
    return render(request, "listings/create.html")


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    return render(request, 'listings/listing.html', {'listing': listing})


@login_required
def watchlist(request):
    return render(request, "listings/watchlist.html")


def categories(request):
    return render(request, "listings/categories.html")
