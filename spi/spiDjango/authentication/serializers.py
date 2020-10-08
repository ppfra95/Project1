from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.password_validation import validate_password

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
        fields = ('email',)


class PasswordTokenSerializer(me_serializers.DocumentSerializer):
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    password2 = serializers.CharField(
        label=_("Repeat password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    token = serializers.CharField()

    class Meta:
        model = User
        fields = ('password', 'password2', 'token')

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        data = self.data
        password = data['password']

        try:
            del(data['password2'])
        except Exception:
            pass

        return  User(**data).set_password(password).save()

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError(
                'Las constraseñas no coinciden', code='password_mismatch'
            )

        validate_password(password)
        return attrs


class TokenSerializer(me_serializers.DocumentSerializer):
    token = serializers.CharField()

    class Meta:
        model = User
        fields = ('token',)
