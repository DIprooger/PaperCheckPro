from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
from rest_framework_simplejwt.exceptions import (
    TokenError,
    InvalidToken
)


from apps.jwt_config.serializers import (
    CustomTokenObtainPairSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "Log-in success",
                "refresh_token": serializer.validated_data.get('refresh'),
                "access_token": serializer.validated_data.get('access')
            }
        )
