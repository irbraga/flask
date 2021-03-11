'''
Module with User database mapping.
'''
import base64
import datetime
from uuid import uuid4
from typing import List
from sqlalchemy import Column, String, Date, DateTime, Enum
from decorators.type import GUID
from extensions.sqlalchemy import db
from entities.types import RoleType


class User(db.Model):
    '''
    User model.
    '''
    __tablename__ = 'users'

    uuid = Column(GUID, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    position = Column(String)
    role = Column(Enum(RoleType), default=RoleType.USER)
    birth = Column(Date, nullable=True)
    username = Column(String, unique=True, nullable=True)
    _password = Column('password', String, nullable=True)
    last_update = Column(DateTime, default=datetime.datetime.now)

    @property
    def password(self):
        '''
        Password property getter.
        '''
        return self._password

    @password.setter
    def password(self, value) -> None:
        '''
        Password setter.
        '''
        self._password = base64.b64encode(value.encode('utf-8'))

    def check_password(self, password: str) -> bool:
        '''
        Return True with the provided password matches with the class password.
        Otherwise, return False.
        '''
        encoded_password = base64.b64encode(password.encode('utf-8'))
        if self._password == encoded_password:
            return True

    @classmethod
    def get_by_uuid(cls, uuid: str) -> 'User':
        '''
        Find a User by UUID.
        '''
        return cls.query.filter_by(uuid = uuid).first()

    @classmethod
    def get_by_username(cls, username: str) -> 'User':
        '''
        Find a User by username.
        '''
        user = cls.query.filter_by(username = username).first()
        if user:
            return user

    @classmethod
    def list_by_role(cls, role: str) -> List['User']:
        '''
        List Users by Role.
        '''
        return cls.query.filter_by(role = role).all()
