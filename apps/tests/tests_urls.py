from rest_framework.reverse import reverse_lazy


class TestUrl:
    def test_auth(self):
        url = reverse_lazy('send_code')
        assert url == '/api/v1/auth/send-code'
        url = reverse_lazy('verify_code')
        assert url == '/api/v1/auth/verify-code'

    def test_product(self):
        pk = 1
        url = reverse_lazy('product_detail', kwargs={'pk': pk})
        assert url == f'/api/v1/products/{pk}'

        url = reverse_lazy('product_list')
        assert url == '/api/v1/products'
