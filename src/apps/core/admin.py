from django.contrib import admin
from .models import *


class FiscalTermAdmin(admin.ModelAdmin):
    list_display = ("semester", "start_date", "end_date", "notes")
    list_filter = ("semester", "start_date", "end_date")
    search_fields = ("semester", "notes")


class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ("category", "value")
    list_filter = ("category",)
    search_fields = ("category", "value")


class BudgetAdmin(admin.ModelAdmin):
    list_display = (
        "category_id_category",
        "category_id_value",
        "fiscal_semester_display",
        "budget",
    )
    list_filter = ("category_id__category", "fiscal__semester")
    search_fields = ("category_id__category", "fiscal__semester", "category_id__value")
    raw_id_fields = ("category_id", "fiscal")

    def category_id_value(self, obj):
        return obj.category_id.value

    category_id_value.short_description = "Value"

    def category_id_category(self, obj):
        return obj.category_id.category

    category_id_category.short_description = "Category"

    def fiscal_semester_display(self, obj):
        return obj.fiscal.semester

    fiscal_semester_display.short_description = "Fiscal Term"


class CashLedgerAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "amount",
        "details",
        "get_budget",
        "get_purpose",
        "transaction_type",
        "notes",
        "account",
        "transaction_id",
        "fiscal",
        "batch_id",
    )
    search_fields = (
        "date",
        "amount",
        "details",
        "transaction_type",
        "notes",
        "account",
        "budget_id__value",
        "purpose_id__value",
        "fiscal__semester",
    )
    list_filter = ("date", "transaction_type", "account", "fiscal__semester", "batch_id",)

    raw_id_fields = ("budget", "purpose", "fiscal")

    def get_budget(self, obj):
        return obj.budget.value

    get_budget.short_description = "Budget Category"

    def get_purpose(self, obj):
        return obj.purpose.value

    get_purpose.short_description = "Purpose Category"


class BankLedgerAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "amount",
        "details",
        "get_budget",
        "get_purpose",
        "transaction_type",
        "opening_balance",
        "closing_balance",
        "notes",
        "transaction_id",
        "fiscal",
        "batch_id",
    )
    search_fields = (
        "date",
        "amount",
        "details",
        "transaction_type",
        "notes",
        "transaction_id",
        "budget_id__value",
        "purpose_id__value",
        "fiscal__semester",
    )
    list_filter = ("date", "transaction_type", "fiscal__semester", "batch_id",)

    raw_id_fields = ("budget", "purpose", "fiscal")

    def get_budget(self, obj):
        return obj.budget.value

    get_budget.short_description = "Budget Category"

    def get_purpose(self, obj):
        return obj.purpose.value

    get_purpose.short_description = "Purpose Category"


class VenmoLedgerAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "type",
        "status",
        "note",
        "from_user",
        "to_user",
        "total_amount",
        "tip_amount",
        "tax_amount",
        "fee_amount",
        "net_amount",
        "tax_rate",
        "tax_exempt",
        "get_budget",
        "funding_source",
        "funding_destination",
        "get_purpose",
        "opening_balance",
        "closing_balance",
        "transaction_type",
        "transaction_id",
        "fiscal",
        "batch_id",
    )
    search_fields = (
        "date",
        "type",
        "status",
        "note",
        "from_user",
        "to_user",
        "total_amount",
        "tip_amount",
        "tax_amount",
        "fee_amount",
        "net_amount",
        "tax_rate",
        "tax_exempt",
        "funding_source",
        "funding_destination",
        "budget_id__value",
        "purpose_id__value",
        "opening_balance",
        "closing_balance",
        "transaction_type",
        "fiscal__semester",
    )
    list_filter = ("date", "type", "status", "transaction_type", "fiscal__semester", "batch_id",)
    raw_id_fields = ("budget", "purpose", "fiscal")

    def get_budget(self, obj):
        return obj.budget.value

    get_budget.short_description = "Budget Category"

    def get_purpose(self, obj):
        return obj.purpose.value

    get_purpose.short_description = "Purpose Category"


class MasterLedgerAdmin(admin.ModelAdmin):
    list_display = (
    'transaction_id', 'date', 'amount', 'transaction_type', 'account', 'budget', 'purpose', 'fiscal_term')
    list_filter = ('transaction_type', 'account', 'budget', 'purpose', 'fiscal_term')
    search_fields = ('transaction_id', 'account', 'budget', 'purpose', 'fiscal_term', 'details')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(FiscalTerm, FiscalTermAdmin)
admin.site.register(TransactionCategory, TransactionCategoryAdmin)
admin.site.register(Budget, BudgetAdmin)
admin.site.register(CashLedger, CashLedgerAdmin)
admin.site.register(BankLedger, BankLedgerAdmin)
admin.site.register(VenmoLedger, VenmoLedgerAdmin)
admin.site.register(MasterLedger, MasterLedgerAdmin)
