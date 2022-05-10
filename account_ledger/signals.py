"""
Contains signals for the account_ledger app.
These signals will update the balance of an account when
a transaction is created.
"""


from django.db.models.signals import post_save
from django.dispatch import receiver


from account_ledger.models import Account, Transaction


@receiver(post_save, sender=Transaction)
def update_account_balance_transaction(sender, instance, created, **kwargs):
    """
    Updates the balance of an account when a transaction is created.
    """
    if created:
        if instance.nature == 'Deposit' or instance.nature == 'Refund':
            instance.account.balance += instance.amount
        else:
            instance.account.balance -= instance.amount
        instance.account.save()


@receiver(post_save, sender=Account)
def update_account_balance(sender, instance, created, **kwargs):
    """
    Updates the balance of an account when an account is created.
    """
    if created:
        instance.balance = instance.balance
        instance.save()
