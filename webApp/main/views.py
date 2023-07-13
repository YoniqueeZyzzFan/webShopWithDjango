from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import *
from django.db.models import Avg
from .forms import RegistrationForm, LoginForm


def update_quantity(request):
    item_id = request.POST.get('item_id')
    action = request.POST.get('action')
    item = get_object_or_404(Item, pk=item_id)
    cart = Cart.objects.get(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if action == 'increment':
        cart_item.quantity += 1
    elif action == 'decrement':
        cart_item.quantity -= 1
    if cart_item.quantity <= 0:
        cart_item.delete()
    else:
        cart_item.save()

    return JsonResponse({'success': True})


def cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = user.cart
        items = cart.cartitem_set.all()
        total = sum(item.get_total_price() for item in items)
    else:
        items = []
        total = 0
    return render(request, 'main/cart.html', {'items': items, 'total': total})


def add_to_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Item, pk=item_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.update_or_create(cart=cart, item=item, defaults={'quantity': 1})
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Cart.objects.create(user=user)
            return redirect('login', register='Registration successful. Please login.')
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = RegistrationForm()

    return render(request, 'main/register.html', {'form': form})


def user_login(request, register=''):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Login failed. Please correct the errors.')
    else:
        form = LoginForm()

    return render(request, 'main/login.html', {'form': form, 'register': register})


def user_logout(request):
    logout(request)
    return redirect('Home')


def index(request):
    average_reviews_count = Item.objects.aggregate(average_reviews_count=Avg('reviews'))['average_reviews_count']
    filtered_items = Item.objects.filter(rating__gte=4.5, reviews__gt=average_reviews_count)[:9]
    items = filtered_items.all()
    return render(request, 'main/index.html', {'items': items})


def catalogue(request, category_id=-1):
    categories = Categories.objects.all()
    if category_id != -1:
        items = Item.objects.filter(category_id=category_id)
    else:
        items = Item.objects.all()
    return render(request, 'main/catalogue.html', {'categories': categories, 'items': items})


def about(request):
    return render(request, 'main/About.html')
