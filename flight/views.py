import random

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
        request.data['number'] = self.get_number(request.data['provider'])

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        number = self.get_number(serializer)
        serializer.save(number=number)

    def get_number(self, provider):
        print(provider)
        provider = provider
        letters = [word[0] for word in provider]
        initial = "".join(letters)
        number = '{}{}'.format(initial, random.randint(100, 999))
        if Flight.objects.filter(number=number).exists():
            number = self.get_number(provider)

        return number


class SingleFlightView(generics.RetrieveUpdateDestroyAPIView):
    """ Generic view for retrieving, updating and deleting a flight """
    permission_classes = (IsAuthenticated,)
    queryset = Flight.objects.filter().all()
    serializer_class = FlightSerializer
    model_name = 'Flight'
