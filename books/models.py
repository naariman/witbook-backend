import uuid

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Book(models.Model):
    READING_STATUS_CHOICES = [
        ('will_read', 'Буду читать'),
        ('now_reading', 'Читаю сейчас'),
        ('finished_reading', 'Прочитана'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_photo = models.ImageField(upload_to='book_photos/', null=True, blank=True)
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    pages_amount = models.IntegerField()
    description = models.TextField()
    reading_status = models.CharField(max_length=20, choices=READING_STATUS_CHOICES)
    star_rate = models.FloatField(null=True, blank=True)
    average_emotion = models.IntegerField(null=True, blank=True)
    current_page = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class ReadingSession(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='sessions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_page = models.IntegerField()
    session_duration = models.IntegerField()
    notes = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    from_page_to_page = models.CharField(max_length=100)
    from_time_to_time = models.CharField(max_length=11, null=True)

    def __str__(self):
        return f"Сессия для {self.book.name} пользователя {self.user.username}"