# Django build-in
from django.core.validators import MinValueValidator
from django.db import models
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

# Local django
from accounts.models import User
from marks.models import AcceptedPlace


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


class PaymentMark(models.Model):
    accountant = models.ForeignKey(
        Accountant,
        on_delete=models.CASCADE,
        verbose_name=_('Accountant')
    )

    accept_mark = models.ForeignKey(
        AcceptedPlace,
        on_delete=models.CASCADE,
        verbose_name=_('Mark'),
    )

    price = models.BigIntegerField(
        validators=[MinValueValidator(0), ],
        default=0,
        verbose_name=_('Price')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created'),
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated'),
    )

    class Meta:
        verbose_name = _('PaymentMark')
        verbose_name_plural = _('PaymentMarks')

    @staticmethod
    def create(request: HttpRequest):
        PaymentMark.objects.create(
            accountant=request.user,
            accept_mark=request.data.get('accept_mark'),
            price=request.data.get('price')
        )

    def __str__(self):
        return F"{self.accountant} - {self.id}"
