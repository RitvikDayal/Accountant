from django.contrib import admin
from django.urls import path, include

from accountant.settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('user_accounts.urls')),
    path('ledger/', include('account_ledger.urls')),
]

if DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
