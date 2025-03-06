from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myapp"


class AccountsConfig(AppConfig): 
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"  

    def ready(self):
        import accounts.signals 
