from datetime import datetime

from django.db.models import Q, Sum
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404, ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import User
from agent.api.v1.serializers import DSOSerializer
from core.api.permissions import IsObjectOwner, IsSuperUser
from core.utils import get_logger
from tracker.api.v1.filters import TransactionFilter, VisitHistoryFilter
from tracker.api.v1.serializers import (
    TransactionDetailsSerializer, TransactionSerializer, VisitHistoryDetailsSerializer,
    VisitHistorySerializer
)
from tracker.models import Transaction, VisitHistory

logger = get_logger()


# noinspection DuplicatedCode
class VisitHistoryListAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filterset_class = VisitHistoryFilter

    def get_serializer_class(self):
        method = self.request.method
        if method == 'GET':
            return VisitHistoryDetailsSerializer
        elif method == 'POST':
            return VisitHistorySerializer

        return super().get_serializer_class()

    def get_queryset(self):
        user: User = self.request.user

        q_exp = Q()
        if not user.is_superuser:
            q_exp = Q(dso__account=user)

        return VisitHistory.objects.filter(q_exp)


class VisitHistoryRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsObjectOwner]
    serializer_class = VisitHistoryDetailsSerializer

    def get_object(self):
        history_id = self.request.query_params.get('id')
        history = get_object_or_404(VisitHistory, id=history_id)
        self.check_object_permissions(self.request, history.dso.account)
        return history


class DailyVisitSummaryAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsSuperUser]
    queryset = VisitHistory.objects.none()
    serializer_class = VisitHistoryDetailsSerializer

    def get(self, request, *args, **kwargs):
        date_str = request.query_params.get('date', str())
        try:
            date = make_aware(datetime.strptime(date_str, '%Y-%m-%d'))
        except (Exception,):
            return Response({'date': ['Enter a valid date.']}, status=status.HTTP_400_BAD_REQUEST)

        # TODO: filter by distributor
        visit_history_qs = VisitHistory.objects.filter(created_date__date=date)
        latest_visit = visit_history_qs.order_by('-created_date').first()

        visit_history_map = {}
        collected_amount_map, distributed_amount_map = {}, {}
        for visit in visit_history_qs:
            collected_amount_map.setdefault(visit.dso, 0)
            distributed_amount_map.setdefault(visit.dso, 0)

            total_collected = Transaction.objects \
                                  .filter(visit_id=visit.id, type=Transaction.TransactionType.COLLECTED) \
                                  .aggregate(total=Sum('amount')) \
                                  .get('total', 0) or 0
            total_distributed = Transaction.objects \
                                    .filter(visit_id=visit.id, type=Transaction.TransactionType.DISTRIBUTED) \
                                    .aggregate(total=Sum('amount')) \
                                    .get('total', 0) or 0

            if visit.dso not in visit_history_map:
                visit_history_map[visit.dso] = set()

            visit_history_map[visit.dso].add(visit.agent.wallet_no)
            collected_amount_map[visit.dso] += total_collected
            distributed_amount_map[visit.dso] += total_distributed

        resp = []
        for dso in visit_history_map.keys():
            resp.append({
                'dso': DSOSerializer(instance=dso).data,
                'total_visited': len(visit_history_map[dso]),
                'total_distributed': distributed_amount_map[dso],
                'total_collected': collected_amount_map[dso],
                'total_agents': dso.agent_set.count(),
                'latest_visit': VisitHistoryDetailsSerializer(instance=latest_visit).data
            })
        return Response(resp, status=status.HTTP_200_OK)


# noinspection DuplicatedCode
class TransactionListAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filterset_class = TransactionFilter

    def get_serializer_class(self):
        method = self.request.method

        if method == 'GET':
            return TransactionDetailsSerializer
        elif method == 'POST':
            return TransactionSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        user: User = self.request.user

        q_exp = Q()
        if not user.is_superuser:
            q_exp = Q(visit__dso__account=user)

        return Transaction.objects.filter(q_exp)


class TransactionRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsObjectOwner]
    serializer_class = TransactionDetailsSerializer

    def get_object(self):
        transaction_id = self.request.query_params.get('id')
        transaction = get_object_or_404(Transaction, id=transaction_id)
        self.check_object_permissions(self.request, transaction.visit.dso.account)
        return transaction
