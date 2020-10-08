import binascii
import os
import datetime

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# from db_conns import MongoEngineConn
from django_mongoengine.mongo_auth.models import User as MongoUser, make_password
from mongoengine import document, fields, CASCADE, signals

from .tokens import get_token_generator
from .myFields import *

# get the token generator class
TOKEN_GENERATOR_CLASS = get_token_generator()

# MongoEngineConn()

__all__ = [
    'ResetPasswordToken',
    'get_password_reset_token_expiry_time',
    'get_password_reset_lookup_field',
    'clear_expired',
    'Token',
]


class Token(document.Document):
    """
    The default authorization token model.
    """
    key = fields.StringField(required=True, max_length=40)
    user = fields.ReferenceField(
        MongoUser, verbose_name='Usuario',
        reverse_delete_rule=CASCADE, null=True
    )
    created = fields.DateTimeField()

    meta = {
        'indexes': ['key', ],
        'collection': 'user_token'
    }

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        if not document.key:
            document.key = document.generate_key()
        if not document.created:
            document.created = datetime.datetime.now()

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key

signals.pre_save.connect(Token.pre_save, sender=Token)


class ResetPasswordToken(document.Document):
    class Meta:
        verbose_name = _("Password Reset Token")
        verbose_name_plural = _("Password Reset Tokens")

    @staticmethod
    def generate_key():
        """ generates a pseudo random code using os.urandom and binascii.hexlify """
        return TOKEN_GENERATOR_CLASS.generate_token()

    # id = models.AutoField(
    #     primary_key=True
    # )

    user = fields.ReferenceField(
        MongoUser,
        related_name='password_reset_tokens',
        reverse_delete_rule=CASCADE,
        verbose_name=_("The User which is associated to this password reset token")
    )

    created_at = fields.DateTimeField(
        verbose_name=_("When was this token generated")
    )

    # Key field, though it is not the primary key of the model
    key = fields.StringField(
        verbose_name=_("Key"),
        max_length=64,
        # db_index=True,
        unique=True
    )

    ip_address = GenericIPAddressField(
        _("The IP address of this session"),
        default="",
        blank=True,
        null=True,
    )

    user_agent = fields.StringField(
        max_length=256,
        verbose_name=_("HTTP User Agent"),
        default="",
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        return super(ResetPasswordToken, self).save(*args, **kwargs)

    def __str__(self):
        return "Password reset token for user {user}".format(user=self.user)

def get_password_reset_token_expiry_time():
    """
    Returns the password reset token expirty time in hours (default: 24)
    Set Django SETTINGS.DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME to overwrite this time
    :return: expiry time
    """
    # get token validation time
    return getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME', 24)


def get_password_reset_lookup_field():
    """
    Returns the password reset lookup field (default: email)
    Set Django SETTINGS.DJANGO_REST_LOOKUP_FIELD to overwrite this time
    :return: lookup field
    """
    return getattr(settings, 'DJANGO_REST_LOOKUP_FIELD', 'email')


def clear_expired(expiry_time):
    """
    Remove all expired tokens
    :param expiry_time: Token expiration time
    """
    ResetPasswordToken.objects.filter(created_at__lte=expiry_time).delete()

# def eligible_for_reset(self):
#     if not self.is_active:
#         # if the user is active we dont bother checking
#         return False
#
#     if getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_REQUIRE_USABLE_PASSWORD', True):
#         # if we require a usable password then return the result of has_usable_password()
#         return self.has_usable_password()
#     else:
#         # otherwise return True because we dont care about the result of has_usable_password()
#         return True
#
# # add eligible_for_reset to the user class
# UserModel = MongoUser
# UserModel.add_to_class("eligible_for_reset", eligible_for_reset)
