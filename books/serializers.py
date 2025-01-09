from rest_framework import serializers
from .models import Book, ReadingSession


class BookSerializer(serializers.ModelSerializer):
    notes_amount = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id',
            'book_photo',
            'name',
            'author',
            'pages_amount',
            'description',
            'reading_status',
            'star_rate',
            'average_emotion',
            'notes_amount',
            'current_page'
        ]

    def get_notes_amount(self, obj):
        return sum(len(session.notes) for session in obj.sessions.all())

    def create(self, validated_data):
        reading_status = validated_data.get('reading_status')
        validated_data['current_page'] = 0
        return super().create(validated_data)


class ReadingSessionSerializer(serializers.ModelSerializer):
    from_page_to_page = serializers.CharField(required=True)
    from_time_to_time = serializers.CharField(required=True)
    created_date = serializers.SerializerMethodField()

    class Meta:
        model = ReadingSession
        fields = ['created_date', 'session_duration',
                  'from_page_to_page', 'from_time_to_time', 'notes', 'current_page']

    def create(self, validated_data):
        book = self.context['book']
        current_page = validated_data.get('current_page', book.current_page)

        if current_page > book.pages_amount:
            raise serializers.ValidationError("Текущая страница не может быть больше общего количества страниц")

        book.current_page = current_page
        if 0 < current_page < book.pages_amount:
            book.reading_status = 'now_reading'
        if current_page == book.pages_amount:
            book.reading_status = 'finished_reading'

        book.save()

        return super().create(validated_data)

    def get_created_date(self, obj):
        return obj.created_at.strftime('%d.%m.%Y')

    def validate_from_time_to_time(self, value):
        import re
        from datetime import datetime

        pattern = r'^([0-2][0-9]):([0-5][0-9])-([0-2][0-9]):([0-5][0-9])$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Время должно быть в формате 'HH:MM-HH:MM' (например, '11:23-12:20')"
            )

        start_time_str, end_time_str = value.split('-')

        try:
            start_time = datetime.strptime(start_time_str, '%H:%M')
            end_time = datetime.strptime(end_time_str, '%H:%M')

            start_hour = int(start_time_str.split(':')[0])
            if start_hour > 23:
                if start_hour > 24:
                    raise serializers.ValidationError(
                        "Час не может быть больше 24"
                    )
        except ValueError:
            raise serializers.ValidationError(
                "Неверный формат времени"
            )

        return value