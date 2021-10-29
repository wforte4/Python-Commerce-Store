from django.contrib.auth.models import AbstractUser
from django.db import models

class Listing(models.Model):
    title = models.CharField(max_length=64)
    desc = models.CharField(max_length=256)
    category = models.CharField(max_length=64, default="Fashion")
    startingprice = models.IntegerField(default=10)
    imageurl = models.CharField(max_length=1000, blank=True, default="https://asset.swarovski.com/images/$size_1000/t_swa103/b_rgb:ffffff,c_scale,dpr_auto,f_auto,w_auto/5408442_png/attract-necklace--round--white--rhodium-plated-swarovski-5408442.png")
    def __str__(self):
        return f"Selling {self.title}"

class User(AbstractUser):
    watching = models.ManyToManyField(Listing, blank=True, related_name="watchlist")

class Bid(models.Model):
    on = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="allbids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usersmakingbids")
    amount = models.IntegerField()
    def __str__(self):
        return f"Bidding on {self.on.title} for {self.amount}"

class Comment(models.Model):
    on = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commentson")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usercommenting")
    desc = models.CharField(max_length=256)
    def __str__(self):
        return f"Bidding on {self.on.title} for {self.amount}"
