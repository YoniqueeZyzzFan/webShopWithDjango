from django.db import models


class Item(models.Model):
    category_id = models.CharField('categoryId', max_length=50)
    title = models.CharField('title', max_length=50)
    price = models.FloatField()
    rating = models.FloatField()
    reviews = models.IntegerField()
    image_link = models.CharField('image_link', max_length=150)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'items'
        verbose_name= 'Item'
        verbose_name_plural = 'Items'