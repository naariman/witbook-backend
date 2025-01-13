from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import Book, ReadingSession
from .serializers import BookSerializer, ReadingSessionSerializer

class BookCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=BookSerializer,
        responses={201: BookSerializer, 400: "Неверные данные"}
    )
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Неверные данные', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class BookListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: BookSerializer(many=True), 401: "Не авторизован"}
    )
    def get(self, request):
        books = Book.objects.filter(user=request.user)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReadingSessionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ReadingSessionSerializer,
        responses={201: ReadingSessionSerializer, 400: "Неверные данные", 404: "Книга не найдена"}
    )
    def post(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id, user=request.user)
        except Book.DoesNotExist:
            return Response({"error": "Книга не найдена"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReadingSessionSerializer(data=request.data, context={'book': book, 'request': request})
        if serializer.is_valid():
            serializer.save(book=book, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Неверные данные', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class BookDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: ReadingSessionSerializer(many=True), 404: "Книга не найдена"}
    )
    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id, user=request.user)
        except Book.DoesNotExist:
            return Response({"error": "Книга не найдена"}, status=status.HTTP_404_NOT_FOUND)

        sessions = book.sessions.all()
        serializer = ReadingSessionSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BookDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id, user=request.user)
        except Book.DoesNotExist:
            return Response({"error": "Книга не найдена"}, status=status.HTTP_404_NOT_FOUND)

        book.delete()
        return Response({"message": "Книга удалена"}, status=status.HTTP_204_NO_CONTENT)