import random

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authentication.models import User
from flight.models import Flight, Seat, Booking


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
        if validated_data.get('seats'):
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
        letters = [word[0] for word in provider.split()]
        initial = "".join(letters)
        number = '{}{}'.format(initial, random.randint(100, 999))
        if Flight.objects.filter(number=number).exists():
            number = self.get_number(provider)

        return number.upper()


class BookingSerializer(serializers.ModelSerializer):

    user = serializers.UUIDField(required=True)
    flight = serializers.UUIDField(required=True)
    seat = SeatSerializer(required=False)

    class Meta:
        model = Booking
        fields = ['flight', 'seat', 'user']

    def create(self, attrs):
        try:
            selected_seat = self.context.get('seat')
            user = User.objects.get(pk=attrs.get('user'))
            flight = Flight.objects.get(pk=attrs.get("flight"))
            if selected_seat:
                seat = flight.seats.get(seat_number=selected_seat)
            else:
                seat = self.auto_select_seat(flight)
            if Booking.objects.filter(flight=flight.id, seat=seat.id, status='active'):
                raise serializers.ValidationError(
                    "This seat is already taken")
            validated_data = {
                "user": user,
                "flight": flight,
                "seat": seat
            }
            return Booking.objects.create(**validated_data)
        except Flight.DoesNotExist:
            raise ValidationError(
                "Flight does not exist")

        except Seat.DoesNotExist:
            raise serializers.ValidationError(
                "Seat does not exist")

    def update(self, instance, attrs):
        try:
            user = User.objects.get(pk=attrs.get('user'))
            flight = Flight.objects.get(pk=attrs.get("flight"))
            validated_data = {
                "user": user,
                "flight": flight,
                "status": 'closed'
            }
            return super().update(instance, validated_data)
        except Flight.DoesNotExist:
            raise ValidationError(
                "Flight does not exist")
        except Seat.DoesNotExist:
            raise serializers.ValidationError(
                "Seat does not exist")

    def auto_select_seat(self, flight):
        booked = list(flight.bookings.filter(status='active').values_list('seat_id', flat=True))
        flight_seats = list(flight.seats.all().values_list('id', flat=True))
        available_seats = []
        for seat in flight_seats:
            if seat not in booked:
                available_seats.append(seat)
        if available_seats:
            return Seat.objects.get(id=random.choices(available_seats)[0])
        raise ValidationError("Sorry, There are no available seats on this Flight")
