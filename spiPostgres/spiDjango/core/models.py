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
