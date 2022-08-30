from rest_framework import serializers

from .models import *


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'color', 'author', 'description', 'is_archive', 'price']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemsSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    book = BookSerializer()

    class Meta:
        model = CartItems
        fields = '__all__'
