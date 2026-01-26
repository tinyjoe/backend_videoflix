from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    """
    Authentication class that retrieves the JWT token from a cookie named 'access_token'.
    """
    def authenticate(self, request):
        """
        The function `authenticate` extracts and validates a token from a request to authenticate a
        user.
        """
        header = self.get_header(request)
        if header is None:
            raw_token = request.COOKIES.get('access_token')
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token