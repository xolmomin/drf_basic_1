import logging

import pytest
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from apps.models import Product

logger = logging.getLogger(__name__)


@pytest.mark.django_db
class TestViews:

    @pytest.fixture(autouse=True)
    def setup_fixture(self):
        self.product_list_url = reverse_lazy('product_list')

    def test_category_list(self, client, category):
        url = reverse_lazy('categories_list')
        response = client.get(url)
        data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert len(data) == 1
        data[0]['name'] = category.name

    def test_product_list_with_pagination(self, client, products):
        page_size = 5
        url = self.product_list_url + '?' + urlencode({'page_size': page_size})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        assert len(response) == 4
        assert len(response['results']) == page_size
        assert response['previous'] is None
        next_page_url = self.product_list_url + '?' + urlencode({'page': 2, 'page_size': page_size})
        assert next_page_url in response['next']

    def test_product_list_with_filter_owner_type(self, client, products):
        logger.info('Product list filter by owner type (starting test) ... ')
        _type = 'admin'
        query = {
            'owner_type': _type
        }
        url = self.product_list_url
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        for product in response['results']:
            assert product['user']['type'] == _type
        logger.info('Product list filter by owner type (ended test) ... ')

    def test_product_list_with_filter_has_image(self, client, products):
        query = {
            'has_image': True
        }
        url = self.product_list_url
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        for product in response['results']:
            assert product['images']
        query = {
            'has_image': False
        }
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        count = Product.objects.count()
        assert response['count'] == count

    def test_product_list_with_filter_price(self, client, products):
        query = {
            'from_price': 1000,
            'to_price': 15000,
        }
        url = self.product_list_url
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        for product in response['results']:
            assert query['from_price'] <= product['price'] <= query['to_price']

    def test_product_list_with_filter_is_premium(self, client, products):
        query = {
            'is_premium': True
        }
        url = self.product_list_url
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        for product in response['results']:
            assert product['is_premium']
        query = {
            'is_premium': False
        }
        url = self.product_list_url
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        for product in response['results']:
            assert not product['is_premium']

    def test_product_list_with_search(self, client, products):
        key = 'ProDucT'
        query = {
            'search': key
        }
        url = self.product_list_url
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        for product in response['results']:
            if key.lower() in product['name'].lower():
                assert key.lower() in product['name'].lower()
            else:
                product = Product.objects.get(id=product['id'])
                assert key.lower() in product.description.lower()

    def test_product_list_with_filter_category(self, client, products, category):
        query = {
            'category': category.id
        }
        url = self.product_list_url
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        for product in response['results']:
            assert product['category'] == category.id
