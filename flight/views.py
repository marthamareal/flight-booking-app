from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from flight.serializers import FlightSerializer
from flight.models import Flight, Seat


class FlightView(generics.ListCreateAPIView):
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

    def perform_create(self, serializer):
        flight = serializer.save()
        seats = []
        for seat in serializer.data['seats']:
            seat['flight'] = flight.id
            seat['seat_number'] = seat
            seats.append(Seat(**seat))
        Seat.objects.bulk_create(seats)


class SingleFlightView(generics.RetrieveUpdateDestroyAPIView):
    """ Generic view for retrieving, updating and deleting a flight """
    permission_classes = (IsAuthenticated,)
    queryset = Flight.objects.filter().all()
    serializer_class = FlightSerializer
    model_name = 'Flight'
