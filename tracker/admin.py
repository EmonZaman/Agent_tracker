from django.contrib import admin

from tracker.models import Transaction, VisitHistory


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass


@admin.register(VisitHistory)
class VisitHistoryAdmin(admin.ModelAdmin):
    pass
