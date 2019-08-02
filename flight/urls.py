from django.urls import path
from . import views


urlpatterns = [
    path('flights/', views.FlightView.as_view(), name='create_and_list_flights'),
    path('flights/<pk>/', views.SingleFlightView.as_view(), name='single_flight'),

    ]

