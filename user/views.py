import logging

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.http import HttpResponse
from jwt import ExpiredSignatureError, DecodeError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer
from .utils import EncodeDecode

logging.basicConfig(filename="view.log", filemode="w")


def index(request):
    return HttpResponse("Welcome to my Book App Management System")


class Signup(APIView):

    def post(self, request):
        """
           Registering new user with name, phone location, email
        """
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = User.objects.create_user(**request.data)
            token = EncodeDecode().encode_token(payload={"id": user.pk})
            url = "http://127.0.0.1:8000/user/validate/" + str(token)
            send_mail("register", url, serializer.data['email'], ['sadanand0275@gmail.com'], fail_silently=False)
            return Response({"message": "data store successfully", "data": {"username": serializer.data}})
        except Exception as e:
            logging.error(e)
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request):
        """
            login existing user with username and password
        """
        try:
            user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
            if user:
                token = EncodeDecode().encode_token(payload={"user_id": user.pk})
                return Response({"message": "login successful", "data": token}, status=status.HTTP_200_OK)
            return Response({"message": "login error", "data": {}}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message": str(e)})


class ValidateToken(APIView):
    """
    Validating the passed token
    """

    def get(self, request, token):
        try:
            decode_token = EncodeDecode().decode_token(token=token)
            user = User.objects.get(id=decode_token.get('id'))
            user.is_verified = True
            user.save()
            return Response({"message": "Validation successfully", "data": user.pk}, status=status.HTTP_201_CREATED)
        except ExpiredSignatureError:
            return Response({"message": "token expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except DecodeError:
            return Response({"message": "wrong token"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
