'''
Module for a type decorator to work with UUID and SQLite3 database.
'''
import uuid
from sqlalchemy.types import TypeDecorator, CHAR

# pylint: disable=abstract-method

class GUID(TypeDecorator):
    '''Platform-independent GUID type.

    Uses CHAR(32), storing as stringified hex values.

    https://docs.sqlalchemy.org/en/13/core/custom_types.html#backend-agnostic-guid-type

    '''
    impl = CHAR

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return '%.32x' % uuid.UUID(value).int
            else:
                return '%.32x' % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value
