from django.urls import path, include


urlpatterns = [
    path('api/', include('user_accounts.api.urls')),
]
