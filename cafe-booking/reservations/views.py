from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Table, Reservation
from .forms import ReservationForm


class TableListView(ListView):
    model = Table
    template_name = 'reservations/table_list.html'
    context_object_name = 'tables'


class TableDetailView(DetailView):
    model = Table
    template_name = 'reservations/table_detail.html'
    context_object_name = 'table'


class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/reservation_form.html'

    def get_initial(self):
        initial = super().get_initial()
        table_id = self.kwargs.get('table_id')
        if table_id:
            initial['table'] = get_object_or_404(Table, id=table_id)
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Ваше бронирование отправлено на подтверждение!')
        return response

    def get_success_url(self):
        return reverse_lazy('table_list')


def reservation_confirmation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if not reservation.confirmed:
        reservation.confirmed = True
        reservation.save()
        messages.success(request, f'Бронирование #{reservation.id} подтверждено!')
    return redirect('admin:reservations_reservation_changelist')