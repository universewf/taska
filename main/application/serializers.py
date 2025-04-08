
from rest_framework import serializers
from .models import Table, Reservation
from datetime import datetime, timedelta
from django.db.models import F

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'name', 'seats', 'location']
        read_only_fields = ['id']

class ReservationSerializer(serializers.ModelSerializer):
    table = TableSerializer(read_only=True)
    table_id = serializers.PrimaryKeyRelatedField(
        queryset=Table.objects.all(),
        source='table',
        write_only=True,
        required=True
    )

    class Meta:
        model = Reservation
        fields = [
            'id',
            'customer_name',
            'table',
            'table_id',
            'reservation_time',
            'duration_minutes'
        ]
        read_only_fields = ['id']

    def validate(self, data):
        # Проверяем пересечение с другими бронями
        table = data['table']
        reservation_time = data['reservation_time']
        duration = data['duration_minutes']

        end_time = reservation_time + timedelta(minutes=duration)#время окончания брони

        # Проверка пересечений с другими бронями
        repeat = Reservation.objects.filter(
            table=table  # Только брони этого столика
        ).exclude(
            pk=self.instance.pk if self.instance else None  # Исключаем текущую запись при обновлении
        ).filter(
            # Условия пересечения временных интервалов:
            # Существующая бронь начинается до окончания новой
            reservation_time__lt=end_time,
            # Существующая бронь заканчивается после начала новой
            reservation_time__gte=reservation_time - timedelta(minutes=duration)
        ).exists()  # Проверяем наличие таких броней

        if repeat:
            raise serializers.ValidationError("Этот столик уже забронирован на указанное время")

        return data  # Возвращаем валидные данные