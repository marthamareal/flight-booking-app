import random

from rest_framework import generics, mixins, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from flight.serializers import FlightSerializer, BookingSerializer
from flight.models import Flight, Booking


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


class BookFlightView(APIView):
    permission_classes = IsAuthenticated,
    serializer_class = BookingSerializer

    def post(self, request, flight):
        request.data["user"] = request.user.id
        request.data["flight"] = flight
        context = {
            "seat": request.data.get('seat')
        }
        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "You have successfully booked flight {0}".format(serializer.data.get('flight'))
        }, status=status.HTTP_201_CREATED)


class CancelBooking(APIView):
    permission_classes = IsAuthenticated,
    serializer_class = BookingSerializer

    def get_booking(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise ValidationError(
                "Booking does not exist")

    def put(self,  request, booking):
        booking = self.get_booking(booking)
        request.data["user"] = request.user.id
        request.data["flight"] = booking.flight.id
        request.data["seat"] = booking.seat
        if request.user != booking.user and not request.user.is_superuser:
            raise ValidationError("Impostor, You can not cancel a booking that does not belong to you")
        if booking.status == 'closed':
            raise ValidationError('You already canceled this booking')
        context = {
            "request": self.request
        }
        serializer = self.serializer_class(data=request.data, context=context, partial=True)
        serializer.instance = booking
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "You have successfully canceled your booking for flight {0}".format(booking.flight)
        }, status=status.HTTP_200_OK)
