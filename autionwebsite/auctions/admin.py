from django.contrib import admin
from .models import Listings,bids,comments, User, category

# Register your models here.
admin.site.register(Listings)
admin.site.register(bids)
admin.site.register(comments)
admin.site.register(User)
admin.site.register(category)