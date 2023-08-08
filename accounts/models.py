# Django build-in
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
# DRF
from django_rest_passwordreset.signals import reset_password_token_created

# Local django
from utils.email_service import send_email


# from .managers import SupervisorManager


class User(AbstractUser):
    class Types(models.TextChoices):
        supervisor = "Supervisor"
        accountant = "Accountant"
        people = "People"

    email = models.CharField(
        max_length=200,
        verbose_name=_('Email'),
        unique=True,
    )
    avatar = models.ImageField(
        upload_to='avatar/',
        verbose_name=_("avatar"),
        null=True,
        blank=True,
    )
    email_active_code = models.CharField(
        max_length=100,
        verbose_name=_("Email-Active-Code")
    )
    token = models.TextField(
        null=True,
        blank=True
    )
    refresh_token = models.TextField(
        null=True,
        blank=True
    )
    user_type = models.CharField(
        choices=Types.choices,
        default=Types.people,
        max_length=100,
        verbose_name=_('Type')
    )
    is_supervisor = models.BooleanField(
        default=False,
        verbose_name=_('Supervisor')
    )
    is_accountant = models.BooleanField(
        default=False,
        verbose_name=_('Accountant')
    )
    is_people = models.BooleanField(
        default=True,
        verbose_name=_('People')
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    groups = models.ManyToManyField(
        Group,
        related_name="user_accounts",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="user_accounts",
        blank=True
    )

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class OtpCode(models.Model):
    email = models.CharField(
        max_length=200,
        verbose_name=_("Email")
    )
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Created")
    )

    def send_gmail(self, email, code):
        send_email(
            subject='Login Verify',
            to=email,
            context={'code': code},
            template_name='emails/Login_verify.html')

    class Meta:
        verbose_name = _("Otp Code")
        verbose_name_plural = _("Otp Codes")

    def __str__(self):
        return f"{self.email} - {self.code} - {self.created}"


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    # context = {
    #     'current_user': reset_password_token.user,
    #     'username': reset_password_token.user.username,
    #     'email': reset_password_token.user.email,
    #     'reset_password_url': "{}?token={}".format(
    #         instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
    #         reset_password_token.key)
    # }

    send_email(
        subject='Reset',
        to=reset_password_token.user.email,
        context={'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key),
            'username': reset_password_token.user.username,
            'email': reset_password_token.user.email,
        },
        template_name='emails/reset_pass.html'
    )
