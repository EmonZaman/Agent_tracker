from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from accounts.models import User, UserRecord
from agent.models import Agent, Distributor, DSO, MA
from core.utils import get_logger
from location.models import Area, District, Division, Region, Union, Upazila

logger = get_logger()


class MASerializer(serializers.ModelSerializer):
    class Meta:
        model = MA
        fields = [
            'id',
            'mobile',
        ]


class DistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        fields = [
            'id',
            'name',
        ]


class DSOSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(label=_('Full Name'), required=False, write_only=True)
    email = serializers.EmailField(label=_('Email'), required=False, write_only=True)
    password = serializers.CharField(label=_('Password'), required=True, write_only=True)

    class Meta:
        model = DSO
        fields = [
            'id',
            'full_name',
            'mobile',
            'email',
            'password',

            'created_date',
            'modified_date',
        ]

    def create(self, validated_data):
        full_name = validated_data.pop('full_name', '')
        email = validated_data.pop('email', '')
        password = validated_data.pop('password', '')

        dso = DSO.objects.create(**validated_data)
        UserRecord.objects.create(email=email, mobile=dso.mobile, password=password)

        user = User.objects.create(username=dso.mobile, email=email, first_name=full_name)
        user.set_password(password)
        user.save()

        dso.account = user
        dso.save()
        return dso


class AgentSerializer(serializers.ModelSerializer):
    distributor = serializers.SlugRelatedField(slug_field='name', queryset=Distributor.objects.all())
    dso = serializers.SlugRelatedField(slug_field='mobile', queryset=DSO.objects.all())
    ma = serializers.SlugRelatedField(slug_field='mobile', queryset=MA.objects.all())
    region = serializers.SlugRelatedField(slug_field='name', queryset=Region.objects.all())
    area = serializers.SlugRelatedField(slug_field='name', queryset=Area.objects.all())
    division = serializers.SlugRelatedField(slug_field='name', queryset=Division.objects.all())
    district = serializers.SlugRelatedField(slug_field='name', queryset=District.objects.all())
    upazila = serializers.SlugRelatedField(slug_field='name', queryset=Upazila.objects.all())
    union = serializers.SlugRelatedField(slug_field='name', queryset=Union.objects.all())

    class Meta:
        model = Agent
        fields = [
            # Basic information
            'id',
            'name',
            'distributor',
            'dso',
            'ma',
            'wallet_no',
            'shop_name',
            'shop_address',
            'qr_string',

            # Status
            'agent_type',
            'status',
            'reg_capability',

            # Location details
            'region',
            'area',
            'division',
            'district',
            'upazila',
            'union',
            'geo_code',

            'reg_date',
            'created_date',
            'modified_date'
        ]
