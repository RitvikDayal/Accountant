from django.contrib import admin

from .models import Account, Transaction, Budget


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'holder', 'balance', 'created_at', 'updated_at')
    list_filter = ('holder',)
    search_fields = (
        'name', 'holder__username',
        'holder__first_name', 'holder__last_name',
    )
    ordering = ('-created_at',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'nature', 'created_at', 'updated_at')
    list_filter = ('account', 'nature')
    search_fields = (
        'account__name', 'account__holder__username',
        'account__holder__first_name', 'account__holder__last_name',
    )
    ordering = ('-created_at',)


class BudgetAdmin(admin.ModelAdmin):
    list_display = ('month', 'created_at', 'updated_at')
    search_fields = ('month',)
    ordering = ('-created_at',)


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Budget, BudgetAdmin)
