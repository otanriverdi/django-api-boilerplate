from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from djoser.conf import settings
from djoser.serializers import UserSerializer
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class GroupUserSerializer(UserSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = tuple(get_user_model().REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'groups',
        )
        read_only_fields = (settings.LOGIN_FIELD,)
