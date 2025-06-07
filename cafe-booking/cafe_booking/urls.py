# cafe_booking/urls.py
from django.contrib import admin
from django.urls import path
from reservations import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.TableListView.as_view(), name='table_list'),
    path('table/<int:pk>/', views.TableDetailView.as_view(), name='table_detail'),
    path('reserve/<int:table_id>/', views.ReservationCreateView.as_view(), name='create_reservation'),
    path('confirm-reservation/<int:pk>/', views.reservation_confirmation, name='confirm_reservation'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)