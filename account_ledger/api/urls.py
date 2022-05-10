from django.urls import path, include


urlpatterns = [
    path('v1/', include('account_ledger.api.v1.urls')),
]
