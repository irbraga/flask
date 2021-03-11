'''
Module with used Enums.
'''
from enum import Enum, unique

@unique
class RoleType(Enum):
    '''
    Enum with supported ROLES.
    '''
    ADMINISTRATOR = 1
    USER = 2
