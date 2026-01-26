from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    confirmed_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password', 'confirmed_password']
        extra_kwargs = {'password': {'write_only': True}, 'email': {'required': True}}

    def validate_confirmed_password(self, value):
        """
        The function `validate_confirmed_password` compares the password and confirmed password values
        and raises a validation error if they do not match.
        """
        password = self.initial_data.get('password')
        if password and value and password != value:
            raise serializers.ValidationError('Passwords do not match')
        return value
    
    def create(self, validated_data):
        """
        The function `create` creates a new user instance with the provided validated data,
        sets the user's password, generates a token, and saves the user to the database.
        """
        validated_data.pop('confirmed_password')
        user = User(username=validated_data['email'],email=validated_data['email'], is_active=False)
        user.set_password(validated_data['password'])
        user.save()
        token = default_token_generator.make_token(user)
        return {'user': user, 'token': token}
    

class LoginTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer to obtain JWT token pair using email and password for authentication.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        """
        The function initializes an object with optional arguments and sets the 'username' field as not
        required.
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False

    def validate(self, attrs):
        """
        The function validates user credentials by checking the email, password, and account activation
        status.
        """
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password')
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid email or password')
        if not user.is_active:
            raise serializers.ValidationError('Account is not activated')
        self.user = user
        return super().validate({'username': user.username, 'password': password})
    

class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        The function `validate_email` checks if a user with the given email exists
        and raises a validation error if not.
        """
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email does not exist')
        return value