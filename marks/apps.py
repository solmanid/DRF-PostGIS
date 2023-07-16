from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MarksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'marks'

    class Meta:
        verbose_name = _('Mark')
        verbose_name_plural = _('Marks')