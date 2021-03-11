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

    @classmethod
    def get_enum_by_name(cls, name:str) -> 'RoleType':
        '''
        Returns a RoleType by it's name.
        '''
        if name:
            for role in RoleType:
                if role.name == name:
                    return role
        raise ValueError(f'{name} is not a valid RoleType name value.')
