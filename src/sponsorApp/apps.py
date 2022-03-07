from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class SponsorappConfig(AppConfig):
    name = 'sponsorApp'
    verbose_name = _('sponsorApp')

    def ready(self):
        import sponsorApp.signals