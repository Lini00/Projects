from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class category(models.Model):
    Field = models.CharField(max_length = 30)
    def __str__(self):
        return self.Field

    
class Listings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    title = models.CharField(max_length = 30)
    description = models.TextField()
    image = models.URLField(max_length = 200, null = True, blank = True)
    category = models.ForeignKey(category, on_delete=models.CASCADE, related_name="cateogry")
    startbid = models.DecimalField(max_digits = 7, decimal_places = 2)
    watchlist = models.ManyToManyField(User, blank = True, related_name ="list")
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.title

class bids(models.Model):
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="biditem")
    currentbid = models.DecimalField(max_digits = 7, decimal_places = 2, blank = True, null = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bider")
    
class comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="item")
    comment = models.TextField(blank = True, null = True)