# import binascii
# import os
# import datetime
#
# from django_mongoengine.mongo_auth.models import AbstractUser
# from mongoengine import document, fields, CASCADE, signals
#
# __all__ = ['Customer']
#
# class Customer(AbstractUser):
#     age=fields.IntField(max_length=3,min_length=1)
#     address = fields.StringField(max_length=30)
#     cell_Phone = fields.IntField(max_length=10,min_length=10)
#
#     def __str__(self):
#         return '%s - %s' % (self.first_name, self.email)
#
#     # def save(self, *args, **kwargs):
#     #     self.password=make_password(self.password)
#     #     self.username=self.email
#     #     if not self.created:
#     #         self.created = datetime.datetime.now()
#     #         # self.url_image=path
#     #     self.updated = datetime.datetime.now()
#     #     return super(Customer, self).save(*args, **kwargs)

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings

from django_rest_passwordreset.signals import reset_password_token_created

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
    print('aqui')
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}/?token={}".format(settings.HTTP_IP_ADDRESS_HEADER,reset_password_token.key)
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
