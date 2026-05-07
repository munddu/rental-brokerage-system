from django.apps import AppConfig
class BrokerageConfig(AppConfig):
    default_auto_field='django.db.models.BigAutoField'
    name='brokerage'
    def ready(self):
        import brokerage.signals
