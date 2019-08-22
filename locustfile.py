import json

from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):

    def on_start(self):
        self.register_user()
        self.login()

    def register_user(self):
        self.client.post('auth/users/',
                         {'email': 'user@gmail.com', 'password': 'P455w0rd'})

    def login(self):
        self.client.post('auth/users/login/',
                         {'email': 'user@gmail.com', 'password': 'P455w0rd'})

    @task(1)
    def show_flights(self):
        self.client.get('flights')

    @task(2)
    def book_flight(self):
        flights_response = self.client.get('flights')
        flights_data = json.loads(flights_response._content)
        if flights_data:
            self.client.post("flights/booking/{flights_data[0]['id']}/")


class APIUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 9000
