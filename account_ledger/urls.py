from django.urls import path, include


urlpatterns = [
    path('api/', include('account_ledger.api.urls')),
]
