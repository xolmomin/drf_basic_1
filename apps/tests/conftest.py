import pytest

from apps.models import Category
from apps.tests.factories import ProductFactory


@pytest.fixture
def category():
    return Category.objects.create(name='Zo\'r Mevalar')


@pytest.fixture
def products():
    return ProductFactory.create_batch(10)
