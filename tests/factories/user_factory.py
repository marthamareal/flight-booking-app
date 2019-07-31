import factory
from faker import Factory

from authentication.models import User

faker = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda _: faker.email())
    first_name = factory.LazyAttribute(lambda _: faker.profile().get('username'))
    last_name = factory.LazyAttribute(lambda _: faker.profile().get('username'))
    phone = factory.LazyAttribute(lambda _: faker.text(20))
    image_url = factory.LazyAttribute(lambda _: faker.text(255))
    password = factory.PostGenerationMethodCall('set_password', 'password123')
