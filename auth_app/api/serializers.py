from django.contrib.auth import get_user_model
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
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields.pop('username')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password')
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid email or password')
        return super().validate(attrs)