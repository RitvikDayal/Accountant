from django.urls import path


from .views import (
    UserLoginView,
    TOTPClientCreateView,
    TOTPClientDeleteView,
    TOTPVerifyView,
    LogoutHandlerView,
)


urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register-2fa/', TOTPClientCreateView.as_view(), name='totp'),
    path('2fa/delete/', TOTPClientDeleteView.as_view(), name='totp_delete'),
    path(
        '2fa/verify/<int:token>', TOTPVerifyView.as_view(), name='totp_verify',
    ),
    path('logout/', LogoutHandlerView.as_view(), name='logout'),
]
