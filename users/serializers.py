from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Position, Sector

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'company', 'position', 'sector']

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
        }


class RegisterSerializer(serializers.ModelSerializer):
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all(), required=False)
    sector = serializers.PrimaryKeyRelatedField(queryset=Sector.objects.all(), required=False)

    class Meta:
        model = User
        fields = [
            'email', 'username', 'password',
            'first_name', 'last_name', 'company', 'position', 'sector'
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
            'email', 'first_name', 'last_name',
            'company', 'position', 'sector', 'profile_picture', 'is_superuser', 'role'  # Agregado el campo profile_picture
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

