from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book, Cart, CartItems
from book.serializers import BookSerializer, CartItemsSerializer
from book.utils import verify_token
from user.models import User


class BookView(APIView):
    """Here performing all crud operation related to book"""

    @verify_token
    def post(self, request):
        """
        Creating adding a book
        :param request: getting request from user
        :return: Response as message and created book
        """
        try:
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "book created successfully", "data": serializer.data},
                                status=status.HTTP_201_CREATED)
            return Response({"message": "book creation failed"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def get(self, request):
        """
        Displaying all books available
        :param request: getting request from user
        :return: Response
        """
        try:
            book = Book.objects.all()
            serializer = BookSerializer(book, many=True)
            return Response({"message": "book found", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def put(self, request):
        """
        Updating book
        :param request: getting value of book id
        :return: Response with updated message and updated book
        """

        try:
            book = Book.objects.get(pk=request.data['id'])
            serializer = BookSerializer(book, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "book updated successfully", "data": serializer.data},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request):
        """
        Deleting book from the database
        :param request: getting value of book id
        :return: Response with deleted message
        """
        try:
            book = Book.objects.get(pk=request.data['id'])
            book.delete()
            return Response({"message": "book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CartView(APIView):
    """Here performing all crud operation related to cart and cart items"""

    @verify_token
    def get(self, request):
        """
        Displaying all items present in the cart
        :param request: getting request from user
        :return: Response
        """
        user_id = request.data.get('user_id')
        cart = Cart.objects.filter(user=user_id, ordered=False).first()
        queryset = CartItems.objects.filter(cart=cart)
        serializer = CartItemsSerializer(queryset, many=True)
        if len(serializer.data) != 0:
            return Response({'message': "Cart found", "data": serializer.data})
        return Response({'message': "Cart is empty"})

    @verify_token
    def post(self, request):
        """
        Creating a cart and Adding items to that cart
        :param request: getting request from user
        :return: Response as message
        """
        data = request.data
        user_id = request.data.get('user_id')
        user = User.objects.get(id=data.get("user_id"))
        cart, _ = Cart.objects.get_or_create(user=user_id, ordered=False)
        book = Book.objects.get(id=data.get('product'))
        price = book.price
        quantity = data.get('quantity')
        cart_items = CartItems(cart=cart, book=book, price=price, quantity=quantity, user=user)
        cart_items.save()

        total_price = 0
        cart_items = CartItems.objects.filter(user=user_id, cart=cart.id)
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({"message": "items added to cart"})

    @verify_token
    def put(self, request):
        """
        Updating the cart and cart items
        :param request: getting value of cart id and quantity
        :return: Response with updated message
        """
        data = request.data
        cart_item = CartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({"message": "Cart updated successfully", })

    @verify_token
    def delete(self, request):
        """
        Deleting item from the cart
        :param request: getting value of cart id
        :return: Response with deleted message
        """
        data = request.data
        cart_item = CartItems.objects.get(id=data.get('id'))
        cart_item.delete()
        return Response({"message": "Item deleted"})
