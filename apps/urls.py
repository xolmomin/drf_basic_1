from django.urls import path
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# from rest_framework.authtoken import views

from apps.views import CategoryListCreateAPIView, VerifyPhoneAPIView, SendPhoneAPIView, ProductListCreateAPIView, \
    ProductRetrieveDestroyAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # path('api-token-auth/', views.obtain_auth_token),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('auth/send-code', SendPhoneAPIView.as_view(), name='send_code'),
    path('auth/verify-code', VerifyPhoneAPIView.as_view(), name='verify_code'),
    path('categories', CategoryListCreateAPIView.as_view(), name='categories_list'),
    path('products', ProductListCreateAPIView.as_view(), name='product_list'),
    path('products/<int:pk>', ProductRetrieveDestroyAPIView.as_view(), name='product_detail'),
]
