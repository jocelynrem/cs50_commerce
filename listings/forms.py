from django import forms
from auctions.models import Bid, Listing, Comment


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]

    def __init__(self, *args, **kwargs):
        self.listing_id = kwargs.pop("listing_id", None)
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")

        if not self.listing_id:
            raise forms.ValidationError("Listing ID is not provided.")

        try:
            listing = Listing.objects.get(pk=self.listing_id)
        except Listing.DoesNotExist:
            raise forms.ValidationError("The listing does not exist.")

        if amount <= listing.starting_bid:
            raise forms.ValidationError("Bid must be greater than the starting bid.")

        highest_bid = listing.bid_set.order_by("-amount").first()
        if highest_bid is not None and amount <= highest_bid.amount:
            raise forms.ValidationError("Bid must be greater than all existing bids.")

        return amount
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        labels = {'comment': 'Leave a comment'}

