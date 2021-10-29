# Generated by Django 3.2.7 on 2021-09-30 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_imageurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='startingprice',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='listing',
            name='imageurl',
            field=models.CharField(blank=True, default='https://asset.swarovski.com/images/$size_1000/t_swa103/b_rgb:ffffff,c_scale,dpr_auto,f_auto,w_auto/5408442_png/attract-necklace--round--white--rhodium-plated-swarovski-5408442.png', max_length=1000),
        ),
    ]