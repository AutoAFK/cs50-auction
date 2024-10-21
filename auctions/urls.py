from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction/<int:auction_id>", views.auction_item, name="auction_item"),
    path("auction/create", views.auction_create, name="auction_create"),
    path("place_bid", views.place_bid, name="place_bid"),
    path(
        "add_to_watchlist/<int:auction_id>",
        views.add_to_watchlist,
        name="add_to_watchlist",
    ),
    path("user", views.user_page, name="user_page"),
]
