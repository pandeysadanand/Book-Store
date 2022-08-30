import jwt


class EncodeDecode:
    """Here encoding and decoding the token"""

    def encode_token(self, payload):
        """
        Taking input payload and encoding that payload
        para payload: it contains data
        return: returning encoded token
        """
        jwt_encode = jwt.encode(payload, "secret", algorithm="HS256")
        return jwt_encode

    def decode_token(self, token):
        """
        Taking input token and decoding that token
        para token: it contains userid
        return: returning decode token
        """
        decode_token = jwt.decode(token, "secret", algorithms=["HS256"])
        return decode_token
