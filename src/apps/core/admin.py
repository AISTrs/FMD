from django.contrib import admin

# Register your models here.
from .models import MasterLedger


class MasterLedgerAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'date', 'details', 'budget', 'purpose', 'account', 'amount', 'transaction_type',)
    list_filter = ('transaction_type', 'date', 'purpose', 'budget', 'account',)
    search_fields = ('purpose', 'budget', 'account',)
    date_hierarchy = 'date'
    ordering = ('-date',)


admin.site.register(MasterLedger, MasterLedgerAdmin)
