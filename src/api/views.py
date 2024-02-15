from django.core.serializers import serialize
from django.http import JsonResponse
from rest_framework.decorators import api_view



@api_view(['GET'])
def get_ledger_data(request):
    # queryset = MasterLedger.objects.all()
    # serialized_data = serialize('json', queryset)
    # return JsonResponse(serialized_data, safe=True)
    return {}
