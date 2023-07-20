from django.apps import AppConfig


class VinodWhatsapp1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vinod_whatsapp1'
    
    def ready(self):
        import vinod_whatsapp1.signals
