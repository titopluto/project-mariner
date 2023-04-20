import factory
from django.contrib.auth import get_user_model
from permission.models import Permission
import uuid
import datetime

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = factory.LazyFunction(uuid.uuid4)
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user{n}")
    given_name = factory.Faker("first_name")
    family_name = factory.Faker("last_name")
    birthdate = factory.Faker("date_of_birth", minimum_age=18)


class PermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Permission

    id = factory.LazyFunction(uuid.uuid4)
    type = factory.Faker("word")
    granted_date = factory.Faker("date_this_year")
    name = factory.Faker("word")
    description = factory.Faker("text")
