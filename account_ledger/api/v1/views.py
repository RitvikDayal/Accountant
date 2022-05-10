from rest_framework import viewsets
from user_accounts.permissions import Is2fa_Authenticated


from account_ledger.api.serializers import (
    AccountSerializer,
    TransactionSerializer,
    BudgetSerializer,
)
from account_ledger.models import Account, Transaction, Budget


class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    permission_classes = (Is2fa_Authenticated,)
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.filter(holder=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or edited.
    """

    permission_classes = (Is2fa_Authenticated,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(account__holder=self.request.user)


class BudgetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows budgets to be viewed or edited.
    """

    permission_classes = (Is2fa_Authenticated,)
    serializer_class = BudgetSerializer

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
