from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories/<int:id>", views.categories, name="categories"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("CreateListing", views.newlisting, name="CreateListing"),
    path("<int:id>", views.item, name="item"),
    path("watch/<int:id>", views.watch, name="watch"),
    path("watchlist", views.displaylist, name = "watchlist"),
    path("bidding/<int:id>", views.bidding, name = "bidding"),
    path("newcomment/<int:id>", views.displaycomments, name = "newcomment"),
    path("close/<int:id>", views.close, name="close")
]
