from rest_framework import serializers

from flight.models import Flight


class FlightSerializer(serializers.ModelSerializer):
    """Flight model serializer"""
    flight_number = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = ('id', 'provider', 'flight_number', 'origin', 'destination',
                  'arrival_time', 'departure_time', 'status', 'created_at', 'updated_at')

        read_only_fields = 'id',

    def get_flight_number(self):
        return 'KQ-LIV2'

    def create(self, data):
        return Flight.objects.create(**data)

    def update(self, instance, validated_data):
        """ Updates a flight from the data provided
        Args:
            instance(object): Flight object updated
            validated_data(dict): a dictionary of validated data of a flight to update
        Returns:
            flight(object): Flight object updated
        """
        flight = super().update(instance, validated_data)
        flight.save()
        return flight
