from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    name = 'aperol.properties'

    def ready(self):
        import aperol.properties.signals
