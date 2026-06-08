# store/apps.py
from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name               = 'store'
    verbose_name       = 'Tienda de Cursos'

    def ready(self):
        import store.signals  # noqa