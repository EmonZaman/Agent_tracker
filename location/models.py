from django.db import models
from django.utils.text import gettext_lazy as _

from core.models import AbstractTimestampModel


class Region(AbstractTimestampModel):
    name = models.CharField(verbose_name=_('Name'), max_length=200)

    class Meta(AbstractTimestampModel.Meta):
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')

    def __str__(self):
        return self.name


class Area(AbstractTimestampModel):
    name = models.CharField(verbose_name=_('Name'), max_length=200)

    class Meta(AbstractTimestampModel.Meta):
        verbose_name = _('Area')
        verbose_name_plural = _('Areas')

    def __str__(self):
        return self.name


class Division(AbstractTimestampModel):
    name = models.CharField(verbose_name=_('Name'), max_length=200)

    class Meta(AbstractTimestampModel.Meta):
        verbose_name = _('Division')
        verbose_name_plural = _('Divisions')

    def __str__(self):
        return self.name


class District(AbstractTimestampModel):
    name = models.CharField(verbose_name=_('Name'), max_length=200)

    class Meta(AbstractTimestampModel.Meta):
        verbose_name = _('District')
        verbose_name_plural = _('Districts')

    def __str__(self):
        return self.name


class Upazila(AbstractTimestampModel):
    name = models.CharField(verbose_name=_('Name'), max_length=200)

    class Meta(AbstractTimestampModel.Meta):
        verbose_name = _('Thana/Upazila')
        verbose_name_plural = _('Thana/Upazila')

    def __str__(self):
        return self.name


class Union(AbstractTimestampModel):
    name = models.CharField(verbose_name=_('Name'), max_length=200)

    class Meta(AbstractTimestampModel.Meta):
        verbose_name = _('Union/Paurashava')
        verbose_name_plural = _('Union/Paurashava')

    def __str__(self):
        return self.name
