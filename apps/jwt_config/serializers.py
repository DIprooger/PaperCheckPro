from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    AuthUser
)

from rest_framework_simplejwt.tokens import Token


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user=user)

        token['email'] = user.email
        token['user_name'] = user.first_name

        return token
