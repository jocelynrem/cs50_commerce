from django.contrib import admin
from .models import User, Listing, Comment, Bid, Category


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

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display these fields in the list view
    search_fields = ['name']  # Allow searching by name



admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category, CategoryAdmin)
