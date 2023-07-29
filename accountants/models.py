# Django build-in
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local django
from accounts.models import User


# Create your models here.


class Accountant(User):
    national_id = models.CharField(
        max_length=11,
        verbose_name=_('National ID'),
        unique=True,
    )
    accountant_code = models.CharField(
        max_length=30,
        verbose_name=_('Accountant Code'),
        unique=True,
    )
    accountant_license = models.ImageField(
        upload_to='supervisor/license/',
        verbose_name=_('License')
    )
    accept_place = models.IntegerField(
        validators=[MinValueValidator, ],
        verbose_name=_('Accepted Place'),
        default=0,
    )

    class Meta:
        verbose_name = _('Accountant')
        verbose_name_plural = _('Accountants')
        # proxy = True

    def save(self, *args, **kwargs):
        self.user_type = User.Types.accountant
        self.is_accountant = True
        self.is_people = False
        return super().save(*args, **kwargs)
