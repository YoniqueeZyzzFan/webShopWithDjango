from django.db import models


class Item(models.Model):
    itemType = models.CharField('itemType', max_length=50)
    title = models.CharField('title', max_length=50)
    price = models.CharField('price', max_length=50)
    rating = models.CharField('rating', max_length=50)
    reviews = models.CharField('reviews', max_length=50)
    imageLink = models.CharField('imageLink', max_length=150)

    def __str__(self):
        return self

    class Meta:
        verbose_name= 'Item'
        verbose_name_plural = 'Items'