import random

from rest_framework import generics, mixins, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from flight.serializers import FlightSerializer, BookingSerializer
from flight.models import Flight, Booking, Seat


class FlightCreateView(mixins.CreateModelMixin, GenericAPIView):
    """ Generic view for creating and listing all flights """
    permission_classes = (IsAuthenticated,)
    queryset = Flight.objects.filter().all()
    serializer_class = FlightSerializer
    model_name = 'Flight'

    def post(self, request, *args, **kwargs):
        """ Method for creating an object"""
        if not request.user.is_superuser:
            raise PermissionDenied(
                "You don't have permissions to create a flight."
            )
        return super().create(request, *args, **kwargs)

    def get_number(self, provider):
        letters = [word[0] for word in provider.split()]
        initial = "".join(letters)
        number = '{}{}'.format(initial, random.randint(100, 999))
        if Flight.objects.filter(number=number).exists():
            number = self.get_number(provider)

        return number.upper()


class FlightListView(mixins.ListModelMixin, GenericAPIView):
    """ Generic view for creating and listing all flights """
    permission_classes = (AllowAny,)
    queryset = Flight.objects.filter().all()
    serializer_class = FlightSerializer
    model_name = 'Flight'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SingleFlightView(generics.RetrieveUpdateDestroyAPIView):
    """ Generic view for retrieving, updating and deleting a flight """
    permission_classes = (IsAuthenticated,)
    queryset = Flight.objects.filter().all()
    serializer_class = FlightSerializer
    model_name = 'Flight'

class BookFlightView(generics.ListCreateAPIView):
    """ Generic view for booking a flight """
    permission_classes = IsAuthenticated,
    serializer_class = BookingSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            flight = Flight.objects.get(pk=self.kwargs.get("pk"))
            seat = flight.seats.get(seat_number=serializer.data.get("seat"))
            if Booking.objects.filter(flight=flight.id, seat=seat.id):
                raise ValidationError(
                    "This seat is already taken")
            serializer.save(user=self.request.user, flight=flight)

        except Flight.DoesNotExist:
            raise ValidationError(
                "Flight does not exist")

        except Seat.DoesNotExist:
            raise ValidationError(
                "Seat does not exist")
