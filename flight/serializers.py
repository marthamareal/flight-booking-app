import random

from rest_framework import serializers

from flight.models import Flight, Seat


class SeatSerializer(serializers.RelatedField):
    """Flight model serializer"""

    def to_internal_value(self, data):
        pass

    def get_queryset(self):
        return Seat.objects.all()

    def to_representation(self, value):
        return value.seat_number


class FlightSerializer(serializers.ModelSerializer):
    """Flight model serializer"""
    seats = SeatSerializer(many=True, required=True)
    number = serializers.CharField(required=False)

    class Meta:
        model = Flight
        fields = ('id', 'provider', 'number', 'origin', 'destination',
                  'arrival_time', 'departure_time', 'status', 'created_at',
                  'updated_at', 'seats')

        read_only_fields = 'id',

    def create(self, data):
        provider = data.get('provider')
        data['number'] = self.get_number(provider)
        request = self.context.get('request')
        del data['seats']  # Recheck this
        seats = request.data.get('seats')
        flight = Flight.objects.create(**data)
        for seat_number in seats:
            try:
                seat = Seat.objects.get(seat_number=seat_number)
                if seat:
                    flight.seats.add(seat.id)
            except Seat.DoesNotExist:
                seat = Seat.objects.create(seat_number=seat_number)
                flight.seats.add(seat.id)

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
        del validated_data['seats']  # Recheck this
        request = self.context.get('request')
        seats = request.data.get('seats')
        flight = super().update(instance, validated_data)
        if seats:
            for seat_number in seats:
                if Flight.objects.filter(seats__seat_number=seat_number):
                    continue
                else:
                    try:
                        seat = Seat.objects.get(seat_number=seat_number)
                        if seat:
                            flight.seats.add(seat.id)
                    except Seat.DoesNotExist:
                        seat = Seat.objects.create(seat_number=seat_number)
                        flight.seats.add(seat.id)

        return flight

    def get_number(self, provider):
        # import pdb; pdb.set_trace()
        letters = [word[0] for word in provider.split()]
        initial = "".join(letters)
        number = '{}{}'.format(initial, random.randint(100, 999))
        if Flight.objects.filter(number=number).exists():
            number = self.get_number(provider)

        return number.upper()
