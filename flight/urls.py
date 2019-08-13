from django.urls import path
from . import views


urlpatterns = [
    path('flights', views.FlightListView.as_view(), name='list_flights'),
    path('flights/create/', views.FlightCreateView.as_view(), name='create_flights'),
    path('flights/<pk>/', views.SingleFlightView.as_view(), name='single_flight'),

    ]

