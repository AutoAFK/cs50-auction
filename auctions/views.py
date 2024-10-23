from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Bid, Comment, Item, WatchList
from .auction import PlaceBidForm, CreateAuctionForm, CreateItemForm


def index(request):
    return render(request, "auctions/index.html", {"auctions": Auction.objects.all()})


def auction_item(request, auction_id):
    # Check for the heighest bid and replace current price with it
    item = Auction.objects.get(id=auction_id)
    current_bid = item.price
    highest_bid = item.auction_bids.order_by("-bid").first().bid or item.price
    if highest_bid > current_bid:
        item.price = highest_bid
        item.save()

    user = request.user
    watchlist_item = user.user_watchlist.filter(auction=item).exists()
    # create a place bid form and set minimum value to the heighest bid.
    form = PlaceBidForm()
    form.fields["amount"].widget.attrs["min"] = item.price
    form.fields["amount"].widget.attrs["value"] = item.price

    return render(
        request,
        "auctions/auction/auction.html",
        {
            "auction": Auction.objects.get(id=auction_id),
            "current_bid": current_bid,
            "place_bid_form": form,
            "is_watchlisted": watchlist_item,
        },
    )


def auction_create(request):
    items_list = Item.objects.all()
    if request.method == "POST":
        user = request.user
        new_auction_form = CreateAuctionForm(request.POST)
        if new_auction_form.is_valid():
            item = new_auction_form.cleaned_data["item"]
            if Item.objects.filter(name=item).exists():
                item = Item.objects.get(name=item)
            price = new_auction_form.cleaned_data["price"]
            auction = Auction(user=user, item=item, price=price)
            auction.save()
            return HttpResponseRedirect(reverse("auction_item", args=[auction.id]))
        return render(
            request,
            "auctions/auction/create.html",
            {
                "new_auction_form": new_auction_form,
                "items_list": items_list,
            },
        )
    else:
        new_auction_form = CreateAuctionForm()
        return render(
            request,
            "auctions/auction/create.html",
            {
                "new_auction_form": new_auction_form,
                "items_list": items_list,
            },
        )


def item_create(request):
    if request.method == "POST":
        new_item_form = CreateItemForm(request.POST)
        if new_item_form.is_valid():
            item_name = new_item_form.cleaned_data["name"]
            if Item.objects.filter(name=item_name).exists():
                return render(
                    request,
                    "auctions/item/create.html",
                    {"new_item_form": new_item_form, "error": "Item already exists."},
                )
            description = new_item_form.cleaned_data["description"]
            item = Item(name=item_name, description=description)
            item.save()
            return HttpResponseRedirect(reverse("auction_create"))
        else:
            return render(
                request,
                "auctions/item/create.html",
                {"new_item_form": new_item_form},
            )
    else:
        new_item_form = CreateItemForm()
        return render(
            request,
            "auctions/item/create.html",
            {"new_item_form": new_item_form},
        )


def place_bid(request):
    if request.method == "POST":
        bid_amount = request.POST["amount"]
        auction_id = request.POST["auction_id"]
        current_price = request.POST["auction_price"]
        user = request.user
        if bid_amount > current_price:
            user_bid = Bid(
                user=user, bid=bid_amount, auction=Auction.objects.get(id=auction_id)
            )
            user_bid.save()
        return HttpResponseRedirect(reverse("auction_item", args=[auction_id]))
    return


def add_to_watchlist(request, auction_id):
    if request.method == "POST":
        user = request.user
        if not user.user_watchlist.filter(auction=auction_id).exists():
            watchlist = WatchList(user=user, auction=Auction.objects.get(id=auction_id))
            watchlist.save()
        else:
            user.user_watchlist.filter(auction=auction_id).delete()
    return HttpResponseRedirect(reverse("auction_item", args=[auction_id]))


def user_page(request):
    user = request.user
    return render(
        request,
        "auctions/user.html",
        {
            "user": user,
            "auctions": user.user_auctions.all(),
            "watchlist": user.user_watchlist.all(),
        },
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
