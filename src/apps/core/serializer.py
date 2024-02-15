from rest_framework import serializers
from .models import FiscalTerm, TransactionCategory, Budget, CashLedger, BankLedger, VenmoLedger, MasterLedger

class FiscalTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiscalTerm
        fields = '__all__'

class TransactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = '__all__'

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'

class CashLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashLedger
        fields = '__all__'

class BankLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankLedger
        fields = '__all__'

class VenmoLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenmoLedger
        fields = '__all__'

class MasterLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterLedger
        fields = '__all__'
