from rest_framework import serializers

from agent.api.v1.serializers import AgentSerializer, DSOSerializer
from agent.models import DSO
from core.utils import get_logger
from tracker.models import Transaction, VisitHistory

logger = get_logger()


class VisitHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitHistory
        fields = [
            'id',
            'dso',
            'agent',
            'note',
            'status',

            'longitude',
            'latitude',

            'created_date',
            'modified_date'
        ]

    def validate(self, attrs):
        user = self.context['request'].user

        if not user.is_superuser:
            """ user is a DSO, assign his profile to dso instance. """
            attrs['dso'] = DSO.objects.get_or_create(account=user)[0]

        return super().validate(attrs)


class VisitHistoryDetailsSerializer(VisitHistorySerializer):
    dso = DSOSerializer(read_only=True)
    agent = AgentSerializer(read_only=True)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id',
            'visit',
            'amount',
            'type',

            'created_date',
            'modified_date'
        ]

    def validate(self, attrs):
        # TODO: validate visit for OwnerPermission.
        return super().validate(attrs)


class TransactionDetailsSerializer(TransactionSerializer):
    visit = VisitHistoryDetailsSerializer(read_only=True)
