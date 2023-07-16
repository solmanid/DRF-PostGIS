# Django build-in
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatar/',
        verbose_name=_("avatar"),
        null=True,
        blank=True,
    )
    email_active_code = models.CharField(max_length=100, verbose_name=_("Email-Active-Code"))
    token = models.TextField(null=True)
    refresh_token = models.TextField(null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    # groups = models.ManyToManyField(Group, related_name="user_accounts", blank=True)
    # user_permissions = models.ManyToManyField(Permission, related_name="user_accounts", blank=True)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class OtpCode(models.Model):
    email = models.CharField(max_length=200, verbose_name=_("Email"))
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True, verbose_name=_("Created"))

    class Meta:
        verbose_name = _("Otp Code")
        verbose_name_plural = _("Otp Codes")

    def __str__(self):
        return f"{self.email} - {self.code} - {self.created}"
