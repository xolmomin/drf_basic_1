from random import randint

from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from apps.filters import ProductFilter
from apps.models import Category, Product
from apps.paginations import CustomPageNumberPagination
from apps.serializers import CategoryModelSerializer, ProductListModelSerializer, ProductDetailModelSerializer, \
    PhoneSerializer, VerifyPhoneSerializer


@extend_schema(tags=['category'])
class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


@extend_schema(tags=['auth'])
class SendPhoneAPIView(GenericAPIView):
    serializer_class = PhoneSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.data['phone_number']
        code = randint(1000, 9999)
        cache.set(phone, code, timeout=120)
        print(f"Nomer: {phone}, Code: {code}")
        return Response({"message": "Successfully sent code"})


@extend_schema(tags=['auth'])
class VerifyPhoneAPIView(GenericAPIView):
    serializer_class = VerifyPhoneSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'OK'})


@extend_schema(tags=['product'])
class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.order_by('id')
    serializer_class = ProductListModelSerializer
    filterset_class = ProductFilter
    pagination_class = CustomPageNumberPagination
    search_fields = 'name', 'description'


@extend_schema(tags=['product'])
class ProductRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailModelSerializer
