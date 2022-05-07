"""
Contains Utilities for the project.
"""


from django_otp.models import Device
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice

from .serializers import TokenPairSerializer


def get_tokens_for_user(user, device=None):
    """
    Get a token pair for a user.

    Parameters
    ----------
    user: User object.
    device: TOTP device object.

    Returns
    -------
    Dictionary of (refresh token, access token).

    """
    serializer = TokenPairSerializer()
    refresh = serializer.get_token(user, device)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def blacklist_tokens(usertoken):
    """
    Logout a user.

    Parameters
    ----------
    usertoken: UserToken object.

    Returns
    -------
    Boolean (True or False) depending upon the successful logout.
    """
    try:
        token = RefreshToken(usertoken)
        token.blacklist()
        return True
    except Exception as e:
        print(e)
        return False


def get_user_totp_device(user, confirmed=None):
    """
    Helper to get the TOTP device for a user.

    Parameters
    ----------
    user: User object.
    confirmed: Boolean (True or False) to filter by
    confirmed or unconfirmed devices.

    Returns
    -------
    TOTP device object.
    """

    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device


def otp_is_verified(self, request):
    """
    Helper to determine if user has verified OTP.

    Parameters
    ----------
    request: Request object.

    Returns
    -------
    Boolean (True or False) depending upon the verification status.
    """
    auth = JWTAuthentication()
    try:
        validation = auth.authenticate(request)
        if validation is not None:
            user, token = validation
            payload = token.payload
            persistent_id = payload.get('otp_device_id')

            if persistent_id:
                device = Device.from_persistent_id(persistent_id)
                if (device is not None) and (device.user_id != request.user.id):  # noqa E501
                    return False
                else:
                    return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
