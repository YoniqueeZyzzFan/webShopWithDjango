from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        db_table = 'custom_user'
        swappable = 'AUTH_USER_MODEL'


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('name', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


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
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
