from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from django_filters import NumberFilter, CharFilter, BooleanFilter, FilterSet, ChoiceFilter

from apps.models import Product, User


class ProductFilter(FilterSet):
    from_price = NumberFilter(field_name='price', lookup_expr='gte')
    to_price = NumberFilter(field_name='price', lookup_expr='lte')
    name = CharFilter(field_name='category__name', lookup_expr='icontains')
    has_image = BooleanFilter(method='has_image_filter')
    owner_type = ChoiceFilter(method='owner_filter', choices=User.Type.choices)
    days = NumberFilter(method='days_filter')

    class Meta:
        model = Product
        fields = ['is_premium', 'category']

    def days_filter(self, queryset, name, value):
        return queryset.filter(created_at__gte=timezone.now() - timedelta(days=int(value)))

    def has_image_filter(self, queryset, name, value):
        if value:
            return queryset.annotate(image_count=Count('images')).filter(image_count__gt=0)
        return queryset

    def owner_filter(self, queryset, name, value):
        return queryset.filter(owner__type=value)
