from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'


class AccountsConfig(AppConfig):  # Change this name if your app is different
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'  # Change 'accounts' to your actual app name

    def ready(self):
        import accounts.signals  # Import the signals module
