from django.urls import path, include


urlpatterns = [
    path('v1/', include('user_accounts.api.v1.urls')),
]
