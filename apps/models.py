from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, IntegerField, TextField, ForeignKey, CASCADE, DateTimeField, ImageField, \
    TextChoices, BooleanField
from mptt.models import MPTTModel, TreeForeignKey

from apps.managers import CustomUserManager

class User(AbstractUser):
    class Type(TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'
        MANAGER = 'manager', 'Manager'
        MODERATOR = 'moderator', 'Moderator'

    balance = IntegerField(db_default=0)
    type = CharField(max_length=25, choices=Type.choices, db_default=Type.USER)
    phone_number = CharField(max_length=25, unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'

    class Meta:
        ordering = 'id',

    def __str__(self):
        return self.phone_number

    def save(self, *args, **kwargs):
        # pre_save
        # self.id, self.pk
        if self.pk is None and (not isinstance(self.balance, int) or self.balance == 0):
            self.balance = 5000
        super().save(*args, **kwargs)
        # post_save

class Category(MPTTModel):
    name = CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        ordering = 'id',


class Product(Model):
    name = CharField(max_length=255)
    price = IntegerField()
    is_premium = BooleanField(db_default=False)
    description = TextField(null=True, blank=True)
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    owner = ForeignKey('apps.User', CASCADE, related_name='products')
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = 'id',


class ProductImage(Model):
    image = ImageField(upload_to='products/')
    product = ForeignKey('apps.Product', CASCADE, related_name='images')

    class Meta:
        ordering = 'id',
