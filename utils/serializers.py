"""
Contains utility serializers for the project.
"""


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TokenPairSerializer(TokenObtainPairSerializer):
    """
    Serializer for TokenObtainPair.

    This is used to get the token pair for the user.
    """

    @classmethod
    def get_token(cls, user, device=None):
        """
        Override get_token method to add custom claims.

        :param user: User object
        :param device: Device object
        :return: Token object
        """
        token = super().get_token(user)

        token['name'] = user.get_full_name
        # custom additions
        if (
            (user is not None)
            and (device is not None)
            and (device.user_id == user.id)
            and (device.confirmed is True)
        ):
            token['otp_device_id'] = device.persistent_id
        else:
            token['otp_device_id'] = None

        if user.is_email_verified is True:
            token['email_verified'] = True
        else:
            token['email_verified'] = False

        return token
