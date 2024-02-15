from django.http import JsonResponse
from rest_framework.decorators import api_view
from apps.core.models import FiscalTerm, Budget, MasterLedger
from apps.core.serializer import FiscalTermSerializer
from django.db.models import Sum


@api_view(["GET"])
def get_fiscal_data(request, fiscal_id=None):
    queryset = FiscalTerm.objects
    if fiscal_id:
        queryset = queryset.filter(id=fiscal_id)

    queryset = queryset.all().order_by("-start_date")
    serializer = FiscalTermSerializer(queryset, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def get_budget_data(request, fiscal_id=None):
    queryset = Budget.objects.select_related("category_id")
    if fiscal_id:
        queryset = queryset.filter(fiscal_id=fiscal_id)

    budget_data = {}
    for budget in queryset:
        if budget.fiscal_id not in budget_data:
            budget_data[budget.fiscal_id] = {}

        budget_data[budget.fiscal_id][budget.category_id.value] = budget.budget

    return JsonResponse(budget_data, safe=False)


@api_view(["GET"])
def get_expense_data(request, fiscal_id=None):
    queryset = MasterLedger.objects
    if fiscal_id:
        queryset = queryset.filter(fiscal_id=fiscal_id)
    queryset = queryset.values(
        "fiscal_id", "budget", "account", "transaction_type"
    ).annotate(amount=Sum("amount"))

    expense_data = {}
    for expense in queryset:

        if expense["fiscal_id"] not in expense_data:
            expense_data[expense["fiscal_id"]] = {}
        if expense["budget"] not in expense_data[expense["fiscal_id"]]:
            expense_data[expense["fiscal_id"]][expense["budget"]] = {}
        if (
            expense["account"]
            not in expense_data[expense["fiscal_id"]][expense["budget"]]
        ):
            expense_data[expense["fiscal_id"]][expense["budget"]][
                expense["account"]
            ] = {}

        expense_data[expense["fiscal_id"]][expense["budget"]][expense["account"]][
            expense["transaction_type"]
        ] = expense["amount"]

    return JsonResponse(expense_data, safe=False)
