from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, CharField
from rest_framework.serializers import ModelSerializer, Serializer
import re
from django.core.cache import cache
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.models import Category, Product, User, ProductImage


class PhoneSerializer(Serializer):
    phone_number = CharField(max_length=255, default='+998 (90) 100 10 10', help_text='Nomer kiriting')

    def validate_phone_number(self, value):
        phone_number = re.sub(r'[^\d]', '', value)
        if len(phone_number) == 12 and phone_number.startswith('998'):
            return phone_number
        raise ValidationError('Nomer normalli emas!')


class VerifyPhoneSerializer(TokenObtainPairSerializer):
    phone_number = CharField(max_length=255, default='+998 90 100 10 10', help_text='Nomer kiriting')
    code = IntegerField(default=4444, help_text='Telefonga kelgan 4xonali codeni kiriting')

    def validate_phone_number(self, value):
        phone_number = re.sub(r'[^\d]', '', value)
        if len(phone_number) == 12 and phone_number.startswith('998'):
            return phone_number
        raise ValidationError('Nomer normalli emas!')

    def validate(self, attrs):
        phone = attrs.get('phone_number')
        code = attrs.get('code')
        cache_code = cache.get(phone)
        if code != cache_code:
            raise ValidationError('Code eskirgan yoki xato!')

        user = User.objects.filter(phone_number=phone).first()
        user.is_active = True
        user.save()
        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'username', 'type'


class ProductImageModelSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = 'id', 'image'


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductListModelSerializer(ModelSerializer):
    images = ProductImageModelSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        exclude = ('description',)

    def to_representation(self, instance: Product):
        repr = super().to_representation(instance)
        repr['user'] = UserModelSerializer(instance.owner).data
        repr['images'] = ProductImageModelSerializer(instance.images, many=True, context=self.context).data
        return repr


class ProductDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ()

    def to_representation(self, instance: Product):
        repr = super().to_representation(instance)
        repr['category'] = CategoryModelSerializer(instance.category).data
        return repr
