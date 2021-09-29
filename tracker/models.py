from django.db import models
from django.utils.text import gettext_lazy as _

from core.models import AbstractTimestampModel


class Transaction(AbstractTimestampModel):
    # region Choices
    class TransactionType(models.TextChoices):
        COLLECTED = 'collected', _('Collected')
        DISTRIBUTED = 'distributed', _('Distributed')

    # endregion

    visit = models.ForeignKey(verbose_name=_('Visit'), to='tracker.VisitHistory', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name=_('Amount'), default=0)
    type = models.CharField(verbose_name=_('Type'), max_length=50, choices=TransactionType.choices)

    class Meta(AbstractTimestampModel.Meta):
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')


class VisitHistory(AbstractTimestampModel):
    # region Choices
    class VisitHistoryStatus(models.TextChoices):
        SUCCESSFUL = 'successful', _('Successful')
        AGENT_ABSENT = 'agent_absent', _('Agent Absent')
        SHOP_CLOSED = 'shop_closed', _('Shop Closed')
        SHOP_RELOCATED = 'shop_relocated', _('Shop Relocated')

    # endregion

    dso = models.ForeignKey(verbose_name=_('DSO'), to='agent.DSO', on_delete=models.CASCADE)
    agent = models.ForeignKey(verbose_name=_('Agent'), to='agent.Agent', on_delete=models.CASCADE)
    note = models.TextField(verbose_name=_('Note'), blank=True)
    status = models.CharField(verbose_name=_('Status'), max_length=50, choices=VisitHistoryStatus.choices)

    # GEO Location
    longitude = models.FloatField(verbose_name=_('Longitude'), default=0.0)
    latitude = models.FloatField(verbose_name=_('Latitude'), default=0.0)

    class Meta(AbstractTimestampModel.Meta):
        verbose_name = _('Visit History')
        verbose_name_plural = _('Visit Histories')
