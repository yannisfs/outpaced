# accounts/apps.py

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Ensures consistency with Django's default
    name = 'accounts'  # Specifies the app's name

    def ready(self):
        """
        This method is called when the app is ready.
        Importing signals here ensures that they are registered when the app starts.
        """
        import accounts.signals  # noqa: F401
