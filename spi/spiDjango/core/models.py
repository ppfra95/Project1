import binascii
import os
import datetime

# from db_conns import MongoEngineConn
from django_mongoengine.mongo_auth.models import User, AbstractUser, make_password
from mongoengine import document, fields, CASCADE, signals


# MongoEngineConn()

# __all__ = ['Token', 'Customer']
__all__ = ['Customer']


# class Token(document.Document):
#     """
#     The default authorization token model.
#     """
#     key = fields.StringField(required=True, max_length=40)
#     user = fields.ReferenceField(
#         User, verbose_name='Usuario',
#         reverse_delete_rule=CASCADE, null=True
#     )
#     created = fields.DateTimeField()
#
#     meta = {
#         'indexes': ['key', ],
#         'collection': 'user_token'
#     }
#
#     @classmethod
#     def pre_save(cls, sender, document, **kwargs):
#         if not document.key:
#             document.key = document.generate_key()
#         if not document.created:
#             document.created = datetime.datetime.now()
#
#     def generate_key(self):
#         return binascii.hexlify(os.urandom(20)).decode()
#
#     def __str__(self):
#         return self.key
#
# signals.pre_save.connect(Token.pre_save, sender=Token)


class Customer(AbstractUser):
    age=fields.IntField(max_length=3,min_length=1)
    address = fields.StringField(max_length=30)
    cell_Phone = fields.IntField(max_length=10,min_length=10)

    def __str__(self):
        return '%s - %s' % (self.first_name, self.email)

    # def save(self, *args, **kwargs):
    #     self.password=make_password(self.password)
    #     self.username=self.email
    #     if not self.created:
    #         self.created = datetime.datetime.now()
    #         # self.url_image=path
    #     self.updated = datetime.datetime.now()
    #     return super(Customer, self).save(*args, **kwargs)
