import random

from rest_framework import generics, mixins, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from flight.serializers import FlightSerializer, BookingSerializer
from flight.models import Flight


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
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CancelBooking(mixins.UpdateModelMixin, GenericAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = BookingSerializer

    def perform_update(self, serializer):
        serializer.save(status='closed')
