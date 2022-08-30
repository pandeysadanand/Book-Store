import logging
from functools import wraps

from rest_framework.response import Response

from user.utils import EncodeDecode

logging.basicConfig(filename="view.log", filemode="w")


def verify_token(function):
    """
        creating function to verify token
    """

    @wraps(function)
    def wrapper(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            response = Response({"message": "Token not provided in header"})
            response.status_code = 401
            logging.info('Token not provided in the header')
            return response
        token = request.META['HTTP_AUTHORIZATION']
        print(token)
        id = EncodeDecode().decode_token(token)
        print(id)
        request.data.update({'user_id': id.get("user_id")})
        print(request.data)
        return function(self, request)

    return wrapper
