from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .services import send_activation_email
from .serializers import RegistrationSerializer, LoginTokenObtainPairSerializer


User = get_user_model()

class RegistrationView(APIView):
    """
    The `RegistrationView` class is an API view for user registration with permission for any user to access.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        This Python function handles POST requests for user registration, validating the data and
        returning appropriate responses.
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            user = result['user']
            token = result['token']
            send_activation_email(user, token)
            return Response({'user': {'id': user.id, 'email': user.email}, 'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccountView(APIView):
    """
    The `ActivateAccountView` class is an API view that handles user account activation.
    """
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        """
        This function activates a user account based on a provided user ID and token,
        returning appropriate responses for success or failure.
        """
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({'detail': 'Activation failed'}, status=status.HTTP_400_BAD_REQUEST)
        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'Activation failed'}, status=status.HTTP_400_BAD_REQUEST)
        if user.is_active:
            return Response({'detail': 'Account already activated'}, status=status.HTTP_200_OK)
        else: 
            user.is_active = True
            user.save()
            return Response({'detail': 'Account activated successfully'}, status=status.HTTP_200_OK)

class LoginView(TokenObtainPairView):
    serializer_class = LoginTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        refresh = serializer.validated_data["refresh"]
        access = serializer.validated_data["access"]
        response = Response({"detail": "Login successful", "user": {"id": serializer.user.id, "username":serializer.user.username}}, status=status.HTTP_200_OK)
        response.set_cookie(key="access", value=access, httponly=True, secure=True, samesite="Lax")
        response.set_cookie(key="refresh", value=refresh, httponly=True, secure=True, samesite="Lax")
        response.data = {"detail": "Login successful"}
        return response
    

class LogoutTokenDeleteView(APIView):
    """
    This class defines a view in a Django REST framework API that handles logging out a user by deleting their access and refresh tokens stored in cookies.
    """
    def post(self, request, *args, **kwargs):
        """
        The function logs out a user by deleting their access and refresh tokens stored in cookies.
        """
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None: 
            return Response({'detail': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        response = Response({'detail': 'Logout successful! All tokens will be deleted. Refresh token is now invalid.'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
    

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh")
        if refresh_token is None: 
            return Response({"detail": "Refresh token not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data={"refresh": refresh_token})
        try: 
            serializer.is_valid(raise_exception=True)
        except:
            return Response({"detail": "Refresh token invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        access_token = serializer.validated_data.get("access")
        response = Response({"detail": "Token refreshed", "access": access_token}, status=status.HTTP_200_OK)
        response.set_cookie(key="access", value=access_token, httponly=True, secure=True, samesite="Lax")
        return response