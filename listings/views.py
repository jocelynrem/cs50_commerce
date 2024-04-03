from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BidForm, CommentForm, ListingForm
from django.http import HttpResponseRedirect
from django.urls import reverse


from auctions.models import Listing, User, Comment, Bid, Category


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
    comments = listing.comments.all()
    bid_form = BidForm(listing_id=listing_id)
    comment_form = CommentForm()

    if request.method == "POST" and request.user.is_authenticated:
        if "submit_bid" in request.POST:
            bid_form = BidForm(request.POST, listing_id=listing_id)
            if bid_form.is_valid():
                bid = bid_form.save(commit=False)
                bid.user = request.user
                bid.listing = listing
                bid.save()
                messages.success(request, "Your bid was successfully placed.")
                return redirect("listings:listing_detail", listing_id=listing_id)
        elif "submit_comment" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.listing = listing
                comment.save()
                messages.success(request, "Your comment was posted.")
                return redirect("listings:listing_detail", listing_id=listing_id)

    # Prepare the context
    context = {
        "listing": listing,
        "form": bid_form,  # Pass the bid form as 'form'
        "highest_bid": highest_bid,
        "comments": comments,
        "comment_form": comment_form,  # Include the initialized or processed comment form
    }
    return render(request, "listings/listing_detail.html", context)


@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user  # Set the current user as the listing owner
            listing.save()
            messages.success(request, 'Your listing has been created successfully.')
            return redirect('index')  # Adjust the redirect as needed
    else:
        form = ListingForm()
    return render(request, 'listings/create_listing.html', {'form': form})



@login_required
def watchlist(request):
    user = request.user
    watchlist_items = user.watchlist.all()  # Get all watchlist items for the user
    return render(request, 'listings/watchlist.html', {'watchlist_items': watchlist_items})


@login_required
def toggle_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if listing.watchers.filter(pk=request.user.pk).exists():
        listing.watchers.remove(request.user)
    else:
        listing.watchers.add(request.user)
    
    # Use the namespaced URL name
    return HttpResponseRedirect(reverse('listings:listing_detail', args=[listing_id]))



def category_list(request):
    categories = Category.objects.all()
    return render(request, "listings/category_list.html", {"categories": categories})


def listings_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = category.listings.filter(active=True)
    return render(request, "listings/listings_by_category.html", {"category": category, "listings": listings})


