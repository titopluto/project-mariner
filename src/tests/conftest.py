import pytest
from .factories import UserFactory, PermissionFactory


@pytest.fixture(scope="function")
def generated_user():
    return UserFactory()


@pytest.fixture(scope="function")
def generated_permission():
    return PermissionFactory()
