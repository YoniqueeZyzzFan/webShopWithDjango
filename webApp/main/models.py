from django.db import models
from django.contrib.auth import get_user_model


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
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
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


class Cart(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='cart'
    )

    def __str__(self):
        return f"Cart for {self.user.username}"

    def get_total(self):
        cart_items = self.cartitem_set.all()
        total = sum(item.get_total_price() for item in cart_items)
        return total

    class Meta:
        db_table = 'cart'
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item.title} - Quantity: {self.quantity}"

    def get_total_price(self):
        return self.quantity * self.item.price

    class Meta:
        db_table = 'cart_item'
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'