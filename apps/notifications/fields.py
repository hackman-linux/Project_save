import uuid
from django.db import models

class BinaryUUIDField(models.BinaryField):
    """Stores a UUID in BINARY(16) for MySQL/MariaDB."""

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 16
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return uuid.UUID(bytes=value)

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value
        if isinstance(value, bytes):
            return uuid.UUID(bytes=value)
        if isinstance(value, str):
            return uuid.UUID(value)
        raise ValueError(f"Cannot convert {value} to UUID")

    def get_prep_value(self, value):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value.bytes
        if isinstance(value, str):
            # Convert string UUID to bytes
            return uuid.UUID(value).bytes
        raise ValueError(f"Cannot convert {value} to bytes for BinaryUUIDField")

    def get_db_prep_value(self, value, connection, prepared=False):
        """This method is called when preparing the value for the database"""
        if prepared:
            return value
        return self.get_prep_value(value)

    def contribute_to_class(self, cls, name, **kwargs):
        """This ensures the field works properly with foreign keys"""
        super().contribute_to_class(cls, name, **kwargs)
        # Set the field's internal type for proper Django handling
        setattr(cls, self.name, self)