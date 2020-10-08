from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from rest_framework import status, serializers, exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import EmailSerializer, PasswordTokenSerializer, TokenSerializer
from .models import ResetPasswordToken, clear_expired, get_password_reset_token_expiry_time, \
    get_password_reset_lookup_field
from .signals import reset_password_token_created, pre_password_reset, post_password_reset

User = get_user_model()

__all__ = [
    'ValidateToken',
    'ResetPasswordConfirm',
    'ResetPasswordRequestToken',
    'reset_password_validate_token',
    'reset_password_confirm',
    'reset_password_request_token'
]

HTTP_USER_AGENT_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_HTTP_USER_AGENT_HEADER', 'HTTP_USER_AGENT')
# HTTP_IP_ADDRESS_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_IP_ADDRESS_HEADER', 'REMOTE_ADDR')



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        # 'reset_password_url': "{}?token={}".format(
        #     instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
        #     reset_password_token.key)
        'reset_password_url': "{}confirm/?token={}".format(reset_password_token.ip_address,reset_password_token.key)
    }
    
    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


class ResetPasswordValidateToken(GenericAPIView):
    """
    An Api View which provides a method to verify that a token is valid
    """
    throttle_classes = ()
    permission_classes = ()
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        # get token validation time
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        if reset_password_token is None:
            return Response({'status': 'notfound'}, status=status.HTTP_404_NOT_FOUND)

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            # delete expired token
            reset_password_token.delete()
            return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'status': 'OK'})


class ResetPasswordConfirm(GenericAPIView):
    """
    An Api View which provides a method to reset a password based on a unique token
    """
    throttle_classes = ()
    permission_classes = ()
    serializer_class = PasswordTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        token = serializer.validated_data['token']

        # get token validation time
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        if reset_password_token is None:
            return Response({'status': 'notfound'}, status=status.HTTP_404_NOT_FOUND)

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            # delete expired token
            reset_password_token.delete()
            return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)

        pre_password_reset.send(sender=self.__class__, user=reset_password_token.user)
        # try:
        #     # validate the password against existing validators
        #     validate_password(
        #         password,
        #         user=reset_password_token.user,
        #         password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
        #     )
        # except ValidationError as e:
        #     # raise a validation error for the serializer
        #     raise exceptions.ValidationError({
        #         'password': e.messages
        #     })

        reset_password_token.user.set_password(password)
        reset_password_token.user.save()
        post_password_reset.send(sender=self.__class__, user=reset_password_token.user)

        # Delete all password reset tokens for this user
        ResetPasswordToken.objects.filter(user=reset_password_token.user).delete()

        # print('aqui')
        return Response({'status': 'OK'})


class ResetPasswordRequestToken(GenericAPIView):
    """
    An Api View which provides a method to request a password reset token based on an e-mail address

    Sends a signal reset_password_token_created when a reset token was created
    """
    throttle_classes = ()
    permission_classes = ()
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # before we continue, delete all existing expired tokens
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # datetime.now minus expiry hours
        now_minus_expiry_time = timezone.now() - timedelta(hours=password_reset_token_validation_time)

        # delete all tokens where created_at < now - 24 hours
        clear_expired(now_minus_expiry_time)

        # find a user by email address (case insensitive search)
        try:
            user = User.objects.get(**{'{}__iexact'.format(get_password_reset_lookup_field()): email})
        except Exception as e:
             raise exceptions.ValidationError({
                    'email': [_(
                        "There is no active user associated with this e-mail address or the password can not be changed")],
                })

        # check if there user that is active
        if user.is_active:
            token = ResetPasswordToken.objects(user=user).upsert_one(user=user)
        else:
            raise exceptions.ValidationError({
                   'email': [_(
                       "There is no active user associated with this e-mail address")],
               })

        # check if the user already has a token
        if not token.key:
            # no token exists, generate a new token
            if settings.DEBUG:
                try:
                    token.ip_address=settings.HTTP_IP_ADDRESS_HEADER+"/password_reset/"
                except Exception as e:
                    token.ip_address=request.META.get('HTTP_HOST')+"/password_reset/"
            else:
                token.ip_address=request.META.get('REMOTE_ADDR')+"/password_reset/"

            token.save()

        # send a signal that the password token was created
        reset_password_token_created.send(sender=self.__class__, instance=self, reset_password_token=token)

        # done
        return Response({'status': 'OK'})


reset_password_validate_token = ResetPasswordValidateToken.as_view()
reset_password_confirm = ResetPasswordConfirm.as_view()
reset_password_request_token = ResetPasswordRequestToken.as_view()
