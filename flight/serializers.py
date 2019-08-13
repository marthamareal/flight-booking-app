import random

from rest_framework import serializers

from flight.models import Flight, Seat


class SeatSerializer(serializers.ModelSerializer):
    """Flight model serializer"""
    class Meta:
        model = Seat
        fields = 'seat_number',


class FlightSerializer(serializers.ModelSerializer):
    """Flight model serializer"""
    seats = SeatSerializer(many=True, required=True)
    number =  serializers.CharField(required=False)
    class Meta:
        model = Flight
        fields = ('id', 'provider', 'number', 'origin', 'destination',
                  'arrival_time', 'departure_time', 'status', 'created_at',
                  'updated_at', 'seats')

        read_only_fields = 'id',

    def create(self, data):
        seats = data.pop('seats')
        flight = Flight.objects.create(**data)
        for seat in seats:
            try:
                seat = Seat.objects.get(seat_number=seat.strip())
                flight.seats.add(seat.id)
            except Seat.DoesNotExist:
                flight.seats.create(seat_number=seat.strip())

        return flight

    def update(self, instance, validated_data):
        """ Updates a flight from the data provided
        Args:
            instance(object): Flight object updated
            validated_data(dict): a dictionary of validated data of
                                a flight to update
        Returns:
            flight(object): Flight object updated
        """
        flight = super().update(instance, validated_data)
        flight.save()
        return flight
