from django import forms
from .models import Reservation
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'customer_name', 'customer_phone', 'customer_email',
                  'date', 'time', 'duration', 'guests']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        table = cleaned_data.get('table')
        duration = cleaned_data.get('duration')

        if date and time and table:
            reservation_datetime = timezone.make_aware(
                datetime.datetime.combine(date, time)
            )

            # Проверка, что бронирование в будущем
            if reservation_datetime < timezone.now():
                raise ValidationError("Нельзя забронировать столик на прошедшее время")

            # Проверка, что столик свободен
            end_time = reservation_datetime + datetime.timedelta(hours=duration)
            overlapping_reservations = Reservation.objects.filter(
                table=table,
                confirmed=True,
                date=date,
                time__lt=end_time.time(),
            ).exclude(
                pk=self.instance.pk if self.instance else None
            )

            for res in overlapping_reservations:
                res_end = datetime.datetime.combine(
                    res.date,
                    res.time
                ) + datetime.timedelta(hours=res.duration)
                if reservation_datetime < res_end:
                    raise ValidationError(
                        f"Столик уже забронирован на это время (до {res_end.time()})"
                    )

        return cleaned_data