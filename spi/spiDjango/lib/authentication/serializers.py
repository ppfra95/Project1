from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework_mongoengine import serializers as me_serializers
from django_mongoengine.mongo_auth.models import User

__all__ = [
    'EmailSerializer',
    'PasswordTokenSerializer',
    'TokenSerializer',
]


class EmailSerializer(me_serializers.DocumentSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email']


class PasswordTokenSerializer(me_serializers.DocumentSerializer):
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})
    token = serializers.CharField()
    #
    # class Meta:
    #     model = User
    #     fields = ('username','email', 'password','password2')


class TokenSerializer(me_serializers.DocumentSerializer):
    token = serializers.CharField()
    #
    # class Meta:
    #     model = User
    #     fields = ('username','email', 'password','password2')
