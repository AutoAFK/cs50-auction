from django.contrib import admin
from .models import Auction, Bid, Item, User

# Register your models here.
admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Item)
