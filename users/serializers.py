from rest_framework import serializers

from witbook import settings
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data.get('username', validated_data['email'])
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=username
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = CustomUser.objects.filter(email=data['email']).first()
        if user and user.check_password(data['password']):
            refresh = RefreshToken.for_user(user)
            access_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            refresh_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

            return {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'access_expires_in': access_lifetime.total_seconds(),
                'refresh_expires_in': refresh_lifetime.total_seconds(),
            }
        raise serializers.ValidationError("Неверный email или пароль")

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'avatar']

class UserRefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        try:
            refresh = RefreshToken(attrs['refresh_token'])
            
            # Get token types from settings
            access_lifetime = settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME')
            refresh_lifetime = settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME')

            # Create new tokens
            access_token = str(refresh.access_token)
            new_refresh_token = str(refresh)

            return {
                'access_token': access_token,
                'refresh_token': new_refresh_token,
                'access_expires_in': int(access_lifetime.total_seconds()),
                'refresh_expires_in': int(refresh_lifetime.total_seconds()),
            }
        except Exception as e:
            raise serializers.ValidationError(
                {
                    'refresh_token': ['Неверный или просроченный refresh token'],
                    'detail': str(e)
                }
            )