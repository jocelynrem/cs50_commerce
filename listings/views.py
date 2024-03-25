from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BidForm


from auctions.models import Listing, User, Comment, Bid


# Create your views here.
def listings(request):
    return render(request, "listings/index.html")


@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id, user=request.user)

    if request.method == "POST" and listing.active:
        # Assuming you have a way to determine the winner, such as the highest bid
        highest_bid = listing.bid_set.order_by("-amount").first()
        if highest_bid:
            listing.winner = highest_bid.user
        listing.active = False
        listing.save()

        # Redirect to the listing detail page or another page as appropriate
        return redirect("listings:listing_detail", listing_id=listing.id)

    # Redirect if the user is not allowed to close the auction or if not POST
    return redirect("listings:listing_detail", listing_id=listing_id)


def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    highest_bid = listing.bid_set.order_by("-amount").first()

    if request.method == "POST" and request.user.is_authenticated:
        form = BidForm(request.POST, listing_id=listing_id)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.user = request.user
            bid.listing = listing
            bid.save()
            messages.success(request, "Your bid was successfully placed.")
            return redirect("listings:listing_detail", listing_id=listing_id)
        else:
            messages.error(request, form.errors)
    else:
        form = BidForm(listing_id=listing_id)

    # Include highest_bid in the context
    context = {
        "listing": listing,
        "form": form,
        "highest_bid": highest_bid,
    }
    return render(request, "listings/listing_detail.html", context)


@login_required
def create(request):
    return render(request, "listings/create.html")


@login_required
def watchlist(request):
    return render(request, "listings/watchlist.html")


def categories(request):
    return render(request, "listings/categories.html")
