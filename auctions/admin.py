from django.contrib import admin
from .models import User, Listing, Comment, Bid


# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "starting_bid",
        "image",
        "category",
        "user",
        "date",
        "active",
        "winner",
    )
    list_filter = ("category", "user", "active", "winner")
    search_fields = ("title", "description", "category")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "comment", "listing", "date")
    list_filter = ("user", "listing")
    search_fields = ("user", "listing")


class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "amount")


admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
