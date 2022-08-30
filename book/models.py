from django.db import models
from django.dispatch import receiver
from user.models import User
from django.db.models.signals import pre_save


class Book(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    author = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    is_archive = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return str(self.user.username) + " " + str(self.total_price)


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.user.username) + " " + str(self.book.name)


@receiver(pre_save, sender=CartItems)
def correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    print(cart_items.user)
    price_of_product = Book.objects.get(id=cart_items.book.id)
    cart_items.price = cart_items.quantity * price_of_product.price
    total_cart_items = CartItems.objects.filter(user=cart_items.user)

    cart = Cart.objects.get(id=cart_items.cart.id)
    cart.total_price = cart_items.price
    cart.save()
















