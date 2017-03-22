from __future__ import unicode_literals
from django.apps import AppConfig

class FirstAppConfig(AppConfig):
    name = 'firstApp'
    verbose_name = 'firstApp for SAM2017'

    def ready(self):
        import firstApp.signals