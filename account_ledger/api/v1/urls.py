from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'accounts', views.AccountViewSet, basename='accounts')
router.register(
    r'transactions', views.TransactionViewSet,
    basename='transactions',
)
router.register(r'budgets', views.BudgetViewSet, basename='budgets')

urlpatterns = [
    path('', include(router.urls)),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
