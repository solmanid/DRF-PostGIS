# Django build-in
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
# Third party
from guardian.models import (
    UserObjectPermissionBase,
    GroupObjectPermissionBase,
    UserObjectPermissionAbstract,
    GroupObjectPermissionAbstract
)
from guardian.shortcuts import assign_perm, remove_perm

# Local django
from accounts.models import User


# Create your models here.

class PlacePoints(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name=_("User")
    )

    picture = models.ImageField(
        null=True,
        blank=True,
        upload_to='upload/ed',
        verbose_name=_('Picture')
    )

    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        null=True,
    )

    location = models.PointField(
        null=True,
        blank=True,
        verbose_name=_('Location')
    )

    likes = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Likes')
    )

    status = models.BooleanField(
        default=True,
        verbose_name=_('Status')
    )

    is_accepted = models.BooleanField(
        default=False,
        verbose_name=_('Accepted')
    )

    created = models.DateField(
        auto_now_add=True,
        verbose_name=_('Created Time')
    )

    class Meta:
        default_permissions = ['add', 'change', 'delete', 'view']
        verbose_name = _("Mark")
        verbose_name_plural = _("Marks")

    def __str__(self):
        return f"{_('User')}: {self.user.username}" \
               f"- {_('Accepted')}: {self.is_accepted} " \
               f"- {_('Description')}:{self.description}" \
               f"- {_('Date')}: {self.created} "


class PlacePointsUserObjectPermission(UserObjectPermissionBase):
    content_object = models.ForeignKey(PlacePoints, on_delete=models.CASCADE)


class PlacePointsGroupObjectPermission(GroupObjectPermissionBase):
    content_object = models.ForeignKey(PlacePoints, on_delete=models.CASCADE)


class BigUserObjectPermission(UserObjectPermissionAbstract):
    id = models.BigAutoField(editable=False, unique=True, primary_key=True)

    class Meta(UserObjectPermissionAbstract.Meta):
        abstract = False
        indexes = [
            *UserObjectPermissionAbstract.Meta.indexes,
            models.Index(fields=['content_type', 'object_pk', 'user']),
        ]


class BigGroupObjectPermission(GroupObjectPermissionAbstract):
    id = models.BigAutoField(editable=False, unique=True, primary_key=True)

    class Meta(GroupObjectPermissionAbstract.Meta):
        abstract = False
        indexes = [
            *GroupObjectPermissionAbstract.Meta.indexes,
            models.Index(fields=['content_type', 'object_pk', 'group']),
        ]


@receiver(post_save, sender=PlacePoints)
def set_permission(sender, instance: PlacePoints, **kwargs):
    permissions = (
        'reporter.view_placepoints',
        'reporter.change_placepoints',
        'reporter.add_placepoints',
        'reporter.delete_placepoints'
    )
    for perm in permissions:
        assign_perm(perm, instance.user, instance)

        if instance.is_accepted:
            remove_perm('reporter.change_placepoints', instance.user, instance)

    assign_perm('view_placepoints', instance.user, instance)
    assign_perm('change_placepoints', instance.user, instance)
    assign_perm('delete_placepoints', instance.user, instance)