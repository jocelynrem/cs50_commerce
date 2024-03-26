from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", related_name="watchers", blank=True)

    def __str__(self):
        return f"{self.username} ({self.email})"

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="won", blank=True, null=True
    )

    def highest_bid(self):
        highest_bid = self.bid_set.aggregate(Max("amount"))["amount__max"]
        if highest_bid is not None:
            return highest_bid
        return None

    def display_bid(self):
        highest_bid = self.highest_bid()
        if highest_bid is not None:
            return f"Highest Bid: ${highest_bid}"
        else:
            return f"Starting Bid: ${self.starting_bid}"

    def __str__(self):
        return f"{self.title} by {self.user}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments"
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} commented on {self.listing} at {self.date}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.amount} by {self.user.username}"
