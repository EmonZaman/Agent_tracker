from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, get_object_or_404, ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.v1.serializers import DeviceSerializer, LoginSerializer, UserRecordSerializer, UserSerializer
from accounts.models import Device, UserRecord
from core.api.permissions import IsSuperUser
from core.utils import get_logger

logger = get_logger()


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        user_info = UserSerializer(user).data
        user_token, _ = Token.objects.get_or_create(user=user)

        response = {
            'token': user_token.key,
            'user_info': user_info
        }
        return Response(response, status=status.HTTP_200_OK)


class UserRecordRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserRecordSerializer
    permission_classes = [IsSuperUser]

    def get_object(self):
        query = self.request.query_params
        mobile = query.get('mobile', '')
        return get_object_or_404(UserRecord, mobile=mobile)


class DeviceApiView(ListCreateAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Device.objects.filter(user=self.request.user)
