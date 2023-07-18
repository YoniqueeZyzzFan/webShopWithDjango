from rest_framework import serializers
from .models import Categories, Item, Cart, CartItem


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    cartitem_set = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'cartitem_set']

    def create(self, validated_data):
        cart_items_data = validated_data.pop('cartitem_set', [])
        cart = Cart.objects.create(**validated_data)
        for cart_item_data in cart_items_data:
            CartItem.objects.create(cart=cart, **cart_item_data)
        return cart

    def update(self, instance, validated_data):
        cart_items_data = validated_data.pop('cartitem_set', [])
        instance.user = validated_data.get('user', instance.user)
        instance.save()

        current_item_ids = set(instance.cartitem_set.values_list('id', flat=True))
        updated_item_ids = [item_data.get('id') for item_data in cart_items_data if item_data.get('id')]
        items_to_delete = current_item_ids - set(updated_item_ids)
        CartItem.objects.filter(id__in=items_to_delete).delete()

        for cart_item_data in cart_items_data:
            item_id = cart_item_data.get('id')
            if item_id:
                cart_item = CartItem.objects.get(pk=item_id, cart=instance)
                cart_item.quantity = cart_item_data.get('quantity', cart_item.quantity)
                cart_item.save()
            else:
                CartItem.objects.create(cart=instance, **cart_item_data)

        return instance
