from django.urls import path
from . import views
from .views import IndexView, CatalogueAPIView

urlpatterns = [
    path('', views.index, name='Home'),
    path('About', views.about, name='About'),
    path('Catalogue/', views.catalogue, name='Catalogue'),
    path('Catalogue/<int:category_id>/', views.catalogue, name='Catalogue'),
    path('Cart', views.cart, name='Cart'),
    path('Register/', views.register, name='Register'),
    path('Login/', views.user_login, name='Login'),
    path('login/<str:register>/', views.user_login, name='login'),
    path('Logout/', views.user_logout, name='Logout'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-quantity/', views.update_quantity, name='update_quantity'),
    path('generate_qr_code', views.generate_qr_code, name='generate_qr_code'),
    path('api/index/', IndexView.as_view(), name='api-index'),
    path('api/catalogue/', CatalogueAPIView.as_view(), name='catalogue-api'),
    path('api/catalogue/<int:category_id>/', CatalogueAPIView.as_view(), name='catalogue-category-api'),
]
