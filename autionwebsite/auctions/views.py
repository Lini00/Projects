from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listings, bids, comments, category

def index(request):
    return render(request, "auctions/index.html", {
        "auctions" : Listings.objects.all(),
        "cateogries" : category.objects.all()
    })

def categories(request, id):
    name = category.objects.get(pk=id)
    items = Listings.objects.filter(category=name)
    if items is not None:
        return render(request, "auctions/cateogries.html",{
            "items" : items,
            "categories": category.objects.all()
        })
    else:
        return render(request, "auctions/cateogries.html",{
            "error" : "No items in this category",
            "categories": category.objects.all()
        })

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def newlisting(request):
    categories = category.objects.all()
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        type = request.POST["type"]
        price = float(request.POST["startbid"])
        image = request.POST["image"]
        cat = category.objects.get(Field = type)
        listing = Listings(title= title, description = description, image = image, category= cat, startbid = price, user=request.user, status =True)
        listing.save()
        bid = bids(item = listing, user = request.user, currentbid = listing.startbid)
        bid.save()
        return render(request, "auctions/CreateListing.html",{
            "categories":categories
        })
    return render(request,"auctions/CreateListing.html",{
        "categories":categories
    })

def item(request, id):
    item = Listings.objects.get(pk=id)
    there = request.user in item.watchlist.all()        
    com = comments.objects.filter(item = item)
    status = item.status
    canclose = item.user == request.user
    bid = bids.objects.get(item=item)
    winner = request.user == bid.user
    return render(request, "auctions/item.html",{
        "item" : item,
        "there": there,
        "com": com,
        "status": status,
        "canclose": canclose,
        "winner": winner
    })

def close(request, id):
    item = Listings.objects.get(pk=id)
    item.status = False
    item.save()
    return HttpResponseRedirect(reverse('item', args=(id, )))

    
def bidding(request, id):
    item = Listings.objects.get(pk = id)
    there = request.user in item.watchlist.all()        
    com = comments.objects.filter(item = item)
    status = item.status
    canclose = item.user == request.user
    if request.method == "POST":
        price = request.POST["price"]
        bid = bids.objects.get(item = item)
        bid.user = request.user
        if float(price) > item.startbid and ((float(price) > bid.currentbid) or (bid.currentbid is None)):
            bid.currentbid = float(price)
            bid.save()
            return render(request, "auctions/item.html",{
                "item" : item,
                "there": there,
                "com": com,
                "status": status,
                "canclose": canclose,
                "message": "Bid was Successful!"
            })
        else:
            return render(request, "auctions/item.html",{
                "item" : item,
                "there": there,
                "com": com,
                "status":status,
                "canclose": canclose,
                "message": "Enter a Higher Price!"
            })
            
    
def displaycomments(request, id):
    item = Listings.objects.get(pk = id)
    if request.method == "POST":
        comment = request.POST["comment"]
        c = comments(user = request.user, item = item, comment = comment)
        c.save()
        return HttpResponseRedirect(reverse('item', args=(id, )))


def displaylist(request):
    user = request.user
    items = user.list.all()
    return render(request, "auctions/watchlist.html",{
        "items" : items
    })

def watch(request, id):
    item = Listings.objects.get(id=id)
    if item.watchlist.filter(id= request.user.id).exists():
        item.watchlist.remove(request.user)
    else:
        item.watchlist.add(request.user)
    return HttpResponseRedirect(reverse('item', args=(id, )))
