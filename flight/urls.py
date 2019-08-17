from django.urls import path
from . import views


urlpatterns = [
    path('flights', views.FlightListView.as_view(), name='list_flights'),
    path('flights/create/', views.FlightCreateView.as_view(), name='create_flights'),
    path('flights/<pk>/', views.SingleFlightView.as_view(), name='single_flight'),
    path('flights/booking/<uuid:flight>/', views.BookFlightView.as_view(), name='book_flight'),
    path('flights/booking/<uuid:booking>/cancel/', views.CancelBooking.as_view(), name='cancel-booking'),
    path('flights/booking/<uuid:flight>/<date>/', views.GetFlightBookings.as_view(), name='get_bookings'),

    ]

