from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Home'),
    path('About', views.about, name='About'),
    path('Catalogue/', views.catalogue, name='Catalogue'),
    path('Catalogue/<int:category_id>/', views.catalogue, name='Catalogue'),
    path('Register/', views.register, name='Register'),
    path('Login/', views.user_login, name='Login'),
    path('Logout/', views.user_logout, name='Logout'),
]
