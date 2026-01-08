from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegistrationSerializer

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
            serializer.save()
            return Response({'detail': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)