from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import gettext_lazy as _

from core.models import AbstractTimestampModel


class User(AbstractUser):
    pass


class UserRecord(AbstractTimestampModel):
    email = models.EmailField(verbose_name=_('Email'), blank=True)
    mobile = models.CharField(verbose_name=_('Mobile'), max_length=20, blank=True)
    password = models.CharField(verbose_name=_('Password'), max_length=128)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)

        if not self.email and not self.mobile:
            error = _(f'At least one of Email and Mobile is required.')
            raise ValidationError(error)

    class Meta(AbstractTimestampModel.Meta):
        verbose_name = _('User Record')
        verbose_name_plural = _('User Records')


class Device(AbstractTimestampModel):
    user = models.ForeignKey(
        verbose_name=_('User'),
        to='accounts.User',
        on_delete=models.CASCADE
    )
    device_id = models.CharField(verbose_name=_('Device ID'), max_length=100)

    class Meta(AbstractTimestampModel.Meta):
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')

    def __str__(self):
        return self.device_id
