from django.apps import AppConfig


class CafecustomerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cafecustomer"

    def ready(self):
        import cafecustomer.signals
