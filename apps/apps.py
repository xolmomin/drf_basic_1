from django.apps import AppConfig


class AppsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps"

    # def ready(self):
    #     from apps.signals import user_post_save
    #
