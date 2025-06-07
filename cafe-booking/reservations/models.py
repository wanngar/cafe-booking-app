from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.validators import MinValueValidator, MaxValueValidator

from cafe_booking import settings


class Table(models.Model):
    TABLE_SHAPES = [
        ('R', 'Прямоугольный'),
        ('O', 'Овальный'),
        ('S', 'Квадратный'),
    ]

    number = models.PositiveIntegerField(unique=True, verbose_name="Номер столика")
    seats = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name="Количество мест"
    )
    shape = models.CharField(max_length=1, choices=TABLE_SHAPES, verbose_name="Форма")
    width = models.FloatField(verbose_name="Ширина (м)")
    length = models.FloatField(verbose_name="Длина (м)")
    image = models.ImageField(
        upload_to='tables/',
        storage=S3Boto3Storage(),
        verbose_name="Фото столика"
    )
    description = models.TextField(blank=True, verbose_name="Описание")

    @property
    def image_url(self):
        """Возвращает полный URL изображения"""
        if self.image:
            return f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{self.image.name}"
        return None

    class Meta:
        verbose_name = "Столик"
        verbose_name_plural = "Столики"

    def __str__(self):
        return f"Столик №{self.number} ({self.get_shape_display()}, {self.seats} мест)"


class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name="Столик")
    customer_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    customer_phone = models.CharField(max_length=20, verbose_name="Телефон клиента")
    customer_email = models.EmailField(verbose_name="Email клиента")
    date = models.DateField(verbose_name="Дата бронирования")
    time = models.TimeField(verbose_name="Время бронирования")
    duration = models.PositiveIntegerField(
        default=2,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        verbose_name="Длительность (часы)"
    )
    guests = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Количество гостей"
    )
    confirmed = models.BooleanField(default=False, verbose_name="Подтверждено")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['-date', '-time']

    def __str__(self):
        return f"Бронирование #{self.id} - {self.customer_name} ({self.date} {self.time})"