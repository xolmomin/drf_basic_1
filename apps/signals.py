# from django.db.models.signals import pre_save, post_save
# from django.dispatch import receiver
#
# from apps.models import User
#
#
# @receiver(pre_save, sender=User)
# def user_post_save(sender, instance: User, **kwargs):
#     if instance.pk is None and (not isinstance(instance.balance, int) or instance.balance == 0):
#         instance.balance = 5000
#
#
# @receiver(post_save, sender=User)
# def user_post_save(sender, instance: User, **kwargs):
#     Favorite.products.create(
#         user=instance,
#         product=Product.objects.first()
#     )
