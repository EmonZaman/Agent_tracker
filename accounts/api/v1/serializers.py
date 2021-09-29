from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from accounts.models import Device, User, UserRecord
from agent.api.v1.serializers import DistributorSerializer, DSOSerializer
from core.utils import get_logger

logger = get_logger()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label=_('Username'), required=True)
    password = serializers.CharField(label=_('Password'), required=True)

    def validate(self, attrs: dict):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(self.context['request'], username=username, password=password)

        if not user:
            raise serializers.ValidationError(_('Invalid credentials!'))

        attrs.update({'user': user})
        return attrs

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class UserSerializer(serializers.ModelSerializer):
    dso_profile = DSOSerializer(read_only=True)
    distributor_profile = DistributorSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_superuser',
            'dso_profile',
            'distributor_profile',

            'date_joined',
        ]


class UserRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRecord
        fields = [
            'id',
            'email',
            'mobile',
            'password',

            'created_date',
            'modified_date',
        ]


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            'id', 'device_id', 'created_date',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        device_id = validated_data.pop('device_id', '')

        Device.objects.filter(user=user).delete()
        device = Device.objects.create(user=user, device_id=device_id)

        return device
