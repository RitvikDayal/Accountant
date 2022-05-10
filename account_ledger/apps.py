from django.apps import AppConfig


class AccountLedgerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account_ledger'

    def ready(self):
        import account_ledger.signals  # noqa: F401
