from django.shortcuts import render
from .models import Item


def index(request):
    items = Item.objects.all()
    print(items)
    return render(request, 'main/index.html', {'items': items})


def about(request):
    return render(request, 'main/About.html')
