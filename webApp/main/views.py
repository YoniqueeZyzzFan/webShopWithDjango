from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import *
from django.db.models import Avg
from .forms import RegistrationForm, LoginForm


def cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = user.cart
        items = cart.cartitem_set.all()
    else:
        items = []
    return render(request, 'main/cart.html', {'items': items})


def add_to_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Item, pk=item_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        CartItem.objects.get_or_create(cart=cart, item=item)
        return JsonResponse({'success': False})
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
