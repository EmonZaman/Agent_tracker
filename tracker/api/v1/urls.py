from django.urls import path

from tracker.api.v1.views import (
    DailyVisitSummaryAPIView, TransactionListAPIView, TransactionRetrieveAPIView, VisitHistoryListAPIView,
    VisitHistoryRetrieveAPIView
)

app_name = 'tracker-api-v1'
urlpatterns = [
    path('visit-histories/', VisitHistoryListAPIView.as_view(), name='visit-history-list'),
    path('visit-histories/item/', VisitHistoryRetrieveAPIView.as_view(), name='visit-history-item'),
    path('visit-histories/summary/', DailyVisitSummaryAPIView.as_view(), name='visit-history-summary'),

    path('transactions/', TransactionListAPIView.as_view(), name='transaction-list'),
    path('transactions/item/', TransactionRetrieveAPIView.as_view(), name='transaction-item'),
]
