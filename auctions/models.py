from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"


class Item(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.name}"


class Auction(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_auctions"
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="item_auctions"
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.item}: {self.price}$"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    bid = models.DecimalField(max_digits=6, decimal_places=2)
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="auction_bids"
    )

    def __str__(self):
        return f"{self.user}: {self.bid}$ on {self.auction.item.name}"


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comments"
    )
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="auction_comments"
    )
    comment = models.CharField(max_length=120)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} on {self.auction.item.name}: {self.comment}"
