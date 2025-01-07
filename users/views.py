from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserRefreshTokenSerializer,
)
from .models import CustomUser

class UserRegistrationView(APIView):
    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={
            201: '{"access_token": "string", "refresh_token": "string"}',
            400: '{"error": "string"}'
        },
        operation_description="Регистрация нового пользователя"
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                }, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'error': f'Ошибка валидации: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': f'Неизвестная ошибка: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Ошибка валидации данных'}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            200: '{"access_token": "string", "refresh_token": "string"}',
            400: '{"error": "string"}'
        },
        operation_description="Авторизация пользователя"
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': f'Ошибка авторизации: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Ошибка валидации данных'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=UserProfileSerializer,
        responses={200: UserProfileSerializer},
        operation_description="Обновление профиля пользователя"
    )
    def post(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': f'Ошибка обновления профиля: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Ошибка валидации данных'}, status=status.HTTP_400_BAD_REQUEST)


class UserRefreshTokenView(APIView):
    @swagger_auto_schema(
        request_body=UserRefreshTokenSerializer,
        responses={
            200: '{"access_token": "string", "refresh_token": "string"}',
            400: '{"error": "string"}'
        },
        operation_description="Обновление токена доступа"
    )
    def post(self, request):
        serializer = UserRefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            try:
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': f'Ошибка обновления токена: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Ошибка валидации данных'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: UserProfileSerializer},
        operation_description="Получение профиля пользователя"
    )
    def get(self, request):
        try:
            serializer = UserProfileSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Ошибка получения профиля: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={204: 'No Content'},
        operation_description="Удаление пользователя"
    )
    def delete(self, request):
        try:
            request.user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': f'Ошибка удаления пользователя: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)