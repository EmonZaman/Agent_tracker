from django.db import models
from django.utils.text import gettext_lazy as _

from core.models import AbstractTimestampModel


class MA(AbstractTimestampModel):
    mobile = models.CharField(verbose_name=_('Mobile'), max_length=20, unique=True)

    class Meta(AbstractTimestampModel.Meta):
        verbose_name = _('MA')
        verbose_name_plural = _('MAs')

    def __str__(self):
        return self.mobile


class Distributor(AbstractTimestampModel):
    name = models.CharField(verbose_name=_('Name'), max_length=200, unique=True)
    account = models.OneToOneField(
        verbose_name=_('User'),
        to='accounts.User',
        related_name='distributor_profile',
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta(AbstractTimestampModel.Meta):
        verbose_name = _('Distributor')
        verbose_name_plural = _('Distributors')

    def __str__(self):
        return self.name


class DSO(AbstractTimestampModel):
    mobile = models.CharField(verbose_name=_('Mobile'), max_length=20, unique=True)
    account = models.OneToOneField(
        verbose_name=_('User'),
        to='accounts.User',
        related_name='dso_profile',
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta(AbstractTimestampModel.Meta):
        verbose_name = _('DSO')
        verbose_name_plural = _('DSOs')

    def __str__(self):
        return self.mobile or super().__str__()


class Agent(AbstractTimestampModel):
    # region Choices
    class AgentType(models.TextChoices):
        AGENT = 'agent', _('Agent')
        BKASH_CARE_AGENT = 'bkash_care_agent', _('bKash Care Agent')
        DAO = 'dao', _('DAO')

    class RegistrationCapability(models.TextChoices):
        NO_REG = 'no_reg', _('No Registration Capability')
        DIGITAL = 'digital', _('Digital')
        DIGITAL_USSD = 'digital_ussd', _('Digital + USSD')

    class AgentStatus(models.TextChoices):
        ACTIVE = 'active', _('Active')
        INACTIVE = 'inactive', _('Inactive')

    # endregion

    # Basic information
    name = models.CharField(verbose_name=_('Name'), max_length=200)
    distributor = models.ForeignKey(
        verbose_name=_('Distributor'),
        to='agent.Distributor',
        null=True,
        on_delete=models.SET_NULL
    )
    dso = models.ForeignKey(
        verbose_name=_('DSO'),
        to='agent.DSO',
        null=True,
        on_delete=models.SET_NULL
    )
    ma = models.ForeignKey(
        verbose_name=_('MA'),
        to='agent.MA',
        null=True,
        on_delete=models.SET_NULL
    )
    wallet_no = models.CharField(verbose_name=_('Wallet No.'), max_length=20)
    shop_name = models.CharField(verbose_name=_('Shop Name'), max_length=200)
    shop_address = models.TextField(verbose_name=_('Shop Address'), blank=True)
    qr_string = models.CharField(verbose_name=_('QR String'), max_length=200, blank=True)

    # Status
    agent_type = models.CharField(
        verbose_name=_('Agent Type'),
        max_length=50,
        choices=AgentType.choices,
        default=AgentType.AGENT
    )
    status = models.CharField(
        verbose_name=_('Status'),
        max_length=50,
        choices=AgentStatus.choices,
        default=AgentStatus.INACTIVE
    )
    reg_capability = models.CharField(
        verbose_name=_('Registration Capability'),
        max_length=50,
        choices=RegistrationCapability.choices,
        default=RegistrationCapability.NO_REG
    )

    # Location details
    region = models.ForeignKey(
        verbose_name=_('Region'),
        to='location.Region',
        null=True,
        blank=False,
        on_delete=models.SET_NULL
    )
    area = models.ForeignKey(
        verbose_name=_('Area'),
        to='location.Area',
        null=True,
        blank=False,
        on_delete=models.SET_NULL
    )
    division = models.ForeignKey(
        verbose_name=_('Division'),
        to='location.Division',
        null=True,
        blank=False,
        on_delete=models.SET_NULL
    )
    district = models.ForeignKey(
        verbose_name=_('District'),
        to='location.District',
        null=True,
        blank=False,
        on_delete=models.SET_NULL
    )
    upazila = models.ForeignKey(
        verbose_name=_('Thana/Upazila'),
        to='location.Upazila',
        null=True,
        blank=False,
        on_delete=models.SET_NULL
    )
    union = models.ForeignKey(
        verbose_name=_('Union/Paurashava'),
        to='location.Union',
        null=True,
        blank=False,
        on_delete=models.SET_NULL
    )
    geo_code = models.CharField(verbose_name=_('GEO Code'), max_length=50, blank=True)
    reg_date = models.DateField(verbose_name=_('Registration Date'), auto_now_add=True)

    class Meta(AbstractTimestampModel.Meta):
        verbose_name = _('Agent')
        verbose_name_plural = _('Agents')

    def __str__(self):
        return self.shop_name
