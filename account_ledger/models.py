import uuid
from django.db import models

from user_accounts.models import User
from utils.choices import Months, Transaction_Type


class Account(models.Model):
    """
    Model to represent an financial account of a user.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    holder = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        unique_together = ('name', 'holder')

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """
    Model to represent a financial transaction.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    nature = models.CharField(
        max_length=100, choices=Transaction_Type, default='Deposit',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return self.account.holder.get_full_name + ' - ' + self.nature + ' - ' + str(self.amount)  # noqa: E501


class Budget(models.Model):
    """
    Model to represent a financial budget.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.CharField(max_length=100, choices=Months, default='January')
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Budget for January, 2020
        return 'Budget for ' + self.month + ', ' + str(self.created_at.year)
