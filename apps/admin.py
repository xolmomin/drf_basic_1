from django.contrib.admin import ModelAdmin
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from apps.models import Category, Product, ProductImage

User = get_user_model()


@admin.register(User)
class UserModelAdmin(UserAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'balance']
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "phone_number", "password1", "password2", "balance"),
            },
        ),
    )


@admin.register(Category)
class CategoryModelAdmin(ModelAdmin):
    pass


@admin.register(ProductImage)
class ProductImageModelAdmin(ModelAdmin):
    pass


@admin.register(Product)
class ProductModelAdmin(ModelAdmin):
    pass
