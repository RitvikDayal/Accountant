from rest_framework import permissions
from django_otp import user_has_device
from utils.utilities import otp_is_verified


class IsAuthenticatedEmailNotVerified(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            bool(
                request.user
                and request.user.is_authenticated
                and request.user.is_active,
            )
            or request.user.is_superuser
        ):
            return True
        return False


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(
            request.user
            and request.user.is_email_verified
            and request.user.is_authenticated
            and request.user.is_active,
        ):
            return True
        return False


class Is2fa_Authenticated(permissions.BasePermission):
    """
    If user has verified TOTP device, require TOTP OTP.
    """

    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        if user_has_device(request.user):
            return (
                IsAuthenticated().has_permission(request, view)
                and otp_is_verified(self, request)
                and request.user.is_active
            )
        else:
            return False
