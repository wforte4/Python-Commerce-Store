from django.contrib import admin

from .models import Bid, Listing, Comment
# Register your models here.

admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(Comment)