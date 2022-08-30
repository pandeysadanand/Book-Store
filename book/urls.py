from book import views
from django.urls import path

urlpatterns = [
    path('book', views.BookView.as_view(), name='register_api'),
    path('cart', views.CartView.as_view(), name='cart_api'),
]
