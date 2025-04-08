from datetime import timedelta
from django.db import models
from django.core.validators import MinValueValidator,MaxLengthValidator
from django.forms import ValidationError
from django.utils import timezone

class Table(models.Model):
    name = models.CharField(max_length=128,unique=True,verbose_name='Название')
    seats = models.IntegerField(verbose_name='Кол-во мест',
                                help_text="Укажите количество посадочных мест",)
    location = models.CharField(verbose_name='Локация',max_length=128,
                                help_text="Например: У окна, Терраса, VIP-зона и т.д.")

    def __str__(self):
        return f"{self.name} ({self.seats} мест, {self.location})"



class Reservation(models.Model):
    customer_name = models.CharField(max_length=200,verbose_name='Имя клиента')
    table = models.ForeignKey(Table,on_delete=models.CASCADE,verbose_name='Столик',related_name='reservations',help_text="Выберите столик для бронирования")
    reservation_time = models.DateTimeField(verbose_name='Время бронирования',db_index=True)
    duration_minutes = models.PositiveIntegerField(verbose_name='Длительность брони',)


    def __str__(self):
        return f"{self.customer_name} - {self.table.name} на {self.reservation_time}"

    def is_table_available(self):
        # Получаем все брони для этого столика
        existing_reservations = Reservation.objects.filter(table=self.table)
        # Время окончания новой брони
        new_end = self.reservation_time + timedelta(minutes=self.duration_minutes)
        for reservation in existing_reservations:
            # Время окончания существующей брони
            existing_end = reservation.reservation_time + timedelta(minutes=reservation.duration_minutes)
            # Проверяем пересечение временных интервалов
            if (self.reservation_time < existing_end and
                new_end > reservation.reservation_time):
                return False
        return True

    def clean(self):
        if not self.is_table_available():#если столиков свободных нет
            raise ValidationError('Этот столик уже занят в указанное время') #райзим ошибку

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)




