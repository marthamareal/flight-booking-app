from datetime import datetime, timedelta

import jwt
from rest_framework import status
from django.urls import reverse

from flight_booking.settings import SECRET_KEY
from tests.factories.flight_factory import FlightFactory, BookingFactory
from tests.factories.seat_factory import SeatFactory
from tests.factories.user_factory import UserFactory
from tests.integration_tests.flight import BaseTestFlight


class TestFlightBooking(BaseTestFlight):
    """Class for testing """

    def test_book_flight_succeeds(self):
        seat = SeatFactory()
        flight = FlightFactory(seats=[seat])
        response = self.client.post(reverse('book_flight', kwargs={'flight': flight.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_flight_invalid_token_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION="invalid")
        flight = FlightFactory()
        response = self.client.get(reverse('get_bookings', kwargs={'flight': flight.id, "date": "2019-08-17"}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_flight_invalid_user_fails(self):
        user = UserFactory()
        payload = {
            "id": str(user.id),
            "first_name": "wrong",
            "exp": datetime.now() + timedelta(days=1)
        }
        token = jwt.encode(payload, SECRET_KEY)
        self.client.credentials(HTTP_AUTHORIZATION=token)
        flight = FlightFactory()
        response = self.client.get(reverse('get_bookings', kwargs={'flight': flight.id, "date": "2019-08-17"}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_flight_with_no_seats_fails(self):
        seat = SeatFactory()
        flight = FlightFactory(seats=[seat])
        self.client.post(reverse('book_flight', kwargs={'flight': flight.id}))
        response = self.client.post(reverse('book_flight', kwargs={'flight': flight.id}),
                                    data={"seat": seat.seat_number}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_flight_with_wrong_id_fails(self):
        seat = SeatFactory()
        response = self.client.post(reverse('book_flight', kwargs={'flight': seat.id}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_flight_with_wrong_seat_fails(self):
        flight = FlightFactory()
        response = self.client.post(reverse('book_flight', kwargs={'flight': flight.id}),
                                    data={"seat": "MJ"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_flight_with_no_available_seat_fails(self):
        seat = SeatFactory()
        flight = FlightFactory(seats=[seat])
        self.client.post(reverse('book_flight', kwargs={'flight': flight.id}))
        response = self.client.post(reverse('book_flight', kwargs={'flight': flight.id}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_booking_succeeds(self):
        flight = FlightFactory()
        user = UserFactory()
        seat = SeatFactory()
        booking = BookingFactory(flight=flight, user=user, seat=seat)
        response = self.client.put(reverse('cancel-booking', kwargs={'booking': booking.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cancel_booking_not_owner_fails(self):
        flight = FlightFactory()
        self.client.post(reverse('book_flight', kwargs={'flight': flight.id}))
        # login another user
        user = UserFactory()
        user_data = {
            "email": user.email,
            "password": "password123"
        }
        login_response = self.client.post(reverse('login'), data=user_data)
        token = login_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.put(reverse('cancel-booking', kwargs={'booking': flight.id}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_booking_with_wrong_id_fails(self):
        flight = FlightFactory()
        response = self.client.put(reverse('cancel-booking', kwargs={'booking': flight.id}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_flight_bookings_admin_succeeds(self):
        flight = FlightFactory()
        response = self.client.get(reverse('get_bookings', kwargs={'flight': flight.id, "date": "2019-08-17"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_flight_bookings_not_admin_fails(self):
        user = UserFactory(is_superuser=False)
        user_data = {
            "email": user.email,
            "password": "password123"
        }
        login_response = self.client.post(reverse('login'), data=user_data)
        token = login_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=token)

        flight = FlightFactory()
        response = self.client.get(reverse('get_bookings', kwargs={'flight': flight.id, "date": "2019-08-17"}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
