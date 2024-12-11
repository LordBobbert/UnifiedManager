# backend/middleware/auth.py

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt

class JWTAuthenticationFromCookie(BaseAuthentication):
    """
    Custom authentication class to authenticate users based on JWT token stored in a cookie.
    """
    def authenticate(self, request):
        # Get the token from the cookie
        token = request.COOKIES.get('access_token')
        if not token:
            return None  # No token found, authentication fails silently
        
        try:
            # Decode the JWT token (replace 'your_secret_key' with your actual key)
            payload = jwt.decode(token, "your_secret_key", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        
        # Retrieve user information from payload (adjust according to your payload structure)
        user_id = payload.get('user_id')
        if not user_id:
            raise AuthenticationFailed('Invalid payload')

        # Perform user lookup (replace with your actual user model lookup)
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
        
        return (user, None)  # Return a tuple of (user, auth)

    def authenticate_header(self, request):
        """
        Returns a WWW-Authenticate header value for 401 responses.
        """
        return 'Bearer'
