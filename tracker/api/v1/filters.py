from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from agent.models import DSO
from tracker.models import Transaction, VisitHistory


class VisitHistoryFilter(filters.FilterSet):
    date = filters.DateFilter(label=_('Date'), field_name='created_date', lookup_expr='date')

    class Meta:
        model = VisitHistory
        fields = ['dso', 'status']


class TransactionFilter(filters.FilterSet):
    dso = filters.ModelChoiceFilter(label=_('DSO'), field_name='visit__dso', queryset=DSO.objects.all())
    date = filters.DateFilter(label=_('Date'), field_name='created_date', lookup_expr='date')

    class Meta:
        model = Transaction
        fields = ['visit', 'type']
