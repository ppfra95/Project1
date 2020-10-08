import ipaddress

from mongoengine import fields

__all__ = [
    'GenericIPAddressField',
]

class GenericIPAddressField(fields.StringField):
    """A field that stores IPV4 and/or IPV6 addresses."""
    IPV4 = 0
    """Accept IPv4 addresses only."""
    IPV6 = 1
    """Accept IPv6 addresses only."""
    BOTH = 2
    """Accept both IPv4 and IPv6 addresses."""

    def __init__(self, verbose_name=None, mongo_name=None, protocol=BOTH,
                 **kwargs):
        """
        :parameters:
          - `verbose_name`: A human-readable name for the Field.
          - `mongo_name`: The name of this field when stored in MongoDB.
          - `protocol`: What protocol this Field should accept. This should be
            one of the following:
            * :attr:`GenericIPAddressField.IPV4`
            * :attr:`GenericIPAddressField.IPV6`
            * :attr:`GenericIPAddressField.BOTH` (default).
        .. seealso:: constructor for
                     :class:`~pymodm.base.fields.MongoBaseField`
        """
        super(GenericIPAddressField, self).__init__(verbose_name=verbose_name,
                                                    mongo_name=mongo_name,
                                                    **kwargs)
        self.protocol = protocol

        # def validate_ip_address(value):
        def validate(self, value):
            if not PY3 and isinstance(value, str):
                value = unicode(value)
            try:
                if GenericIPAddressField.IPV4 == self.protocol:
                    ipaddress.IPv4Address(value)
                elif GenericIPAddressField.IPV6 == self.protocol:
                    ipaddress.IPv6Address(value)
                elif GenericIPAddressField.BOTH == self.protocol:
                    ipaddress.ip_address(value)
            except (ValueError, ipaddress.AddressValueError):
                raise ValidationError('%r is not a valid IP address.' % value)
        # self.validators.append(validate_ip_address)
