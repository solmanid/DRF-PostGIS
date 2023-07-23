# Django build-in
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.signals import reset_password_token_created

from utils.email_service import send_email


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatar/',
        verbose_name=_("avatar"),
        null=True,
        blank=True,
    )
    email_active_code = models.CharField(max_length=100, verbose_name=_("Email-Active-Code"))
    token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    groups = models.ManyToManyField(Group, related_name="user_accounts", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="user_accounts", blank=True)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class OtpCode(models.Model):
    email = models.CharField(max_length=200, verbose_name=_("Email"))
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True, verbose_name=_("Created"))

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
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

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
    #
    # # render email text
    # email_html_message = render_to_string('emails/user_reset_password.html', context)
    # email_plaintext_message = render_to_string('emails/user_reset_password.txt', context)
    #
    # msg = EmailMultiAlternatives(
    #     # title:
    #     "Password Reset for {title}".format(title="Some website title"),
    #     # message:
    #     email_plaintext_message,
    #     # from:
    #     "sandbox.smtp.mailtrap.io",
    #     # to:
    #     [reset_password_token.user.email]
    # )
    # msg.attach_alternative(email_html_message, "text/html")
    # msg.send()
    #
