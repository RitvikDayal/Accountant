"""
Contains version: 1 of the User Accounts API for
Login, Registration and Logout.
"""


from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.permissions import AllowAny

from django_otp import user_has_device

from user_accounts.api.serializers import UserLoginSerializer
from user_accounts.permissions import (
    IsAuthenticated,
    Is2fa_Authenticated,
)
from utils.utilities import (
    get_user_totp_device,
    blacklist_tokens,
    get_tokens_for_user,
)


class UserLoginView(generics.GenericAPIView):
    """
    Login the User for 1st Factor Authentication.
    Issues a jwt token to the user.
    """
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Login the user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        response = Response()

        response.data = {
            'status': 'success',
            'message': 'User logged in successfully.',
            'token': validated_data['access_token'],
            'username': validated_data['user_name'],
        }

        response.set_cookie(
            key='refresh-token',
            value=serializer.validated_data['refresh_token'],
            httponly=True,
            samesite='lax',
            path='/',
            secure=True,
        )

        response.status_code = status.HTTP_200_OK

        return response


class TOTPClientCreateView(views.APIView):
    """
    Add a new TOTP totp_device for a user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get the TOTP totp_device for the current user.
        Setup a new TOTP totp_device for a user if it does not exist.
        """
        user = request.user

        if user_has_device(user):
            return Response(
                {'success': 'True', 'message': '2FA already configured!'},
                status=status.HTTP_204_NO_CONTENT,
            )

        else:

            device = get_user_totp_device(user, confirmed=False)

            if device:
                return Response(
                    {
                        'success': 'True',
                        'oauth_url': device.config_url,
                        # "secret_key": device.key, #should not be here
                    },
                    status=status.HTTP_200_OK,
                )

            else:
                totp_device = user.totpdevice_set.create(confirmed=False)
                return Response(
                    {
                        'success': 'True',
                        'oauth_url': totp_device.config_url,
                    },
                    status=status.HTTP_201_CREATED,
                )


class TOTPClientDeleteView(views.APIView):
    """
    Delete the TOTP totp_device for a user.
    """

    permission_classes = [Is2fa_Authenticated]

    def get(self, request):
        """
        Delete the TOTP totp_device for the current user.
        """
        user = request.user

        if user_has_device(user):
            user.totpdevice_set.all().delete()
            return Response(
                {'success': 'True', 'message': '2FA deleted successfully!'},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {'success': 'False', 'message': '2FA not configured!'},
                status=status.HTTP_204_NO_CONTENT,
            )


class TOTPVerifyView(views.APIView):
    """
    Verify the TOTP token for the current user.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, token):
        """
        Verify the TOTP token for the current user.

        Args:
            token (str): The TOTP token to verify.

        Returns:
            Response: The response object.
        """
        user = request.user
        totp_device = get_user_totp_device(user)

        if totp_device and totp_device.verify_token(token):
            if not totp_device.confirmed:
                totp_device.confirmed = True
                totp_device.save()

            refresh_token = request.COOKIES.get('refresh-token')

            blacklist_prev_refresh_token = blacklist_tokens(refresh_token)

            if blacklist_prev_refresh_token:
                response = Response()

                response.status_code = status.HTTP_200_OK
                token = get_tokens_for_user(user, totp_device)

                response.data = {
                    'token': token['access'],
                }

                response.set_cookie(
                    key='refresh-token',
                    value=token['refresh'],
                    httponly=True,
                    samesite='lax',
                    path='/',
                    secure=True,
                )

                return response
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutHandlerView(views.APIView):
    """
    View for logging out a user
    """

    permission_classes = (Is2fa_Authenticated,)

    def post(self, request):
        """
        POST request to logout a user
        """

        refresh_token = request.COOKIES.get('refresh-token')

        blacklist_current_refresh_token = blacklist_tokens(refresh_token)

        if blacklist_current_refresh_token:
            response = {
                'success': 'True',
                'message': 'User logged out successfully',
            }
            status_code = status.HTTP_200_OK
        else:
            response = {
                'success': 'False',
                'message': 'User not logged out',
            }
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(response, status=status_code)
