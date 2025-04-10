from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .models import PasswordResetToken
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import User, Position, Sector

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'company', 'position', 'sector']

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'title']  # Campos para la posición


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'name']  # Campos para el sector


class LoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def validate(self, data):
        email_or_username = data.get('email_or_username')
        password = data.get('password')

        # Autenticar con el backend personalizado
        user = authenticate(username=email_or_username, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': self.get_tokens(user),
            'role': user.role
        }


class RegisterSerializer(serializers.ModelSerializer):
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all(), required=False)
    sector = serializers.PrimaryKeyRelatedField(queryset=Sector.objects.all(), required=False)
    password = serializers.CharField(
            write_only=True, 
            min_length=8, 
            error_messages={
                'min_length': 'La contraseña debe tener al menos 8 caracteres.'
            }
        )
    class Meta:
        model = User
        fields = [
            'email', 'username', 'password',
            'company', 'position', 'sector'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    position = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(),
        required=False,
        allow_null=True
    )
    sector = serializers.PrimaryKeyRelatedField(
        queryset=Sector.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = [
            'email', 'username',
            'company', 'position', 'sector', 'profile_picture', 'is_superuser', 'role', 'company_relation', 'location'  # Agregado el campo profile_picture
        ]
        read_only_fields = ['email']

    def validate_position(self, value):
        # Si es vacío o nulo, devuelve None
        if value == "" or value is None:
            return None
        return value

    def validate_sector(self, value):
        # Si es vacío o nulo, devuelve None
        if value == "" or value is None:
            return None
        return value

    def validate_profile_picture(self, value):
        # Validación para asegurarse de que sea una cadena base64
        if value and not isinstance(value, str):
            raise serializers.ValidationError("El formato de la imagen no es válido.")
        return value

    def validate(self, attrs):
        # Aplica validaciones adicionales si es necesario
        attrs['position'] = self.validate_position(attrs.get('position'))
        attrs['sector'] = self.validate_sector(attrs.get('sector'))
        attrs['profile_picture'] = self.validate_profile_picture(attrs.get('profile_picture'))
        return attrs

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True)
    
    def validate_new_password(self, value):
        try:
            password_validation.validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value