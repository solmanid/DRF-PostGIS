# Django build-in
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local django
from accounts.models import User


# Create your models here.


class Supervisor(User):
    national_id = models.CharField(
        max_length=11,
        verbose_name=_('National ID'),
        unique=True
    )
    supervisor_code = models.CharField(
        max_length=30,
        verbose_name=_('Supervisor Code'),
        unique=True,
    )
    supervisor_license = models.ImageField(
        upload_to='supervisor/license/',
        verbose_name=_('License')
    )
    accept_place = models.IntegerField(
        validators=[MinValueValidator, ],
        verbose_name=_('Accepted Place'),
        default=0,
    )

    # objects = SupervisorManager

    class Meta:
        verbose_name = _('Supervisor')
        verbose_name_plural = _('Supervisors')

    #     proxy = True

    def save(self, *args, **kwargs):
        self.user_type = User.Types.supervisor
        self.is_supervisor = True
        self.is_people = False
        return super().save(*args, **kwargs)
