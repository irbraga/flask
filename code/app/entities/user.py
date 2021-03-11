'''
Module with User database mapping.
'''
import base64
import datetime
from uuid import uuid4, UUID
from typing import List
import dateutil
from sqlalchemy import Column, String, Date, DateTime, Enum
from app.decorators.type import GUID
from app.extensions.sqlalchemy import db
from app.entities.types import RoleType

# pylint: disable=too-many-instance-attributes

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

    def __init__(self, uuid: UUID=None, name: str=None, position: str=None,
                    role: RoleType=None, birth: datetime.date=None,
                    username: str=None, password: str=None,
                    last_update: datetime.datetime=None) -> 'User':
        '''
        Constructor of an instance.
        '''
        self.uuid = uuid
        self.name = name
        self.position = position
        self.username = username
        self.password = password

        if role:
            if isinstance(role, str):
                self.role = RoleType.get_enum_by_name(role)
            else:
                self.role = role

        if birth:
            if isinstance(birth, str):
                self.birth = dateutil.parser.parse(birth)
            else:
                self.birth = birth

        if last_update:
            if isinstance(last_update, str):
                self.last_update = dateutil.parser.parse(last_update)
            else:
                self.last_update = last_update

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
    def find_by_uuid(cls, uuid: str) -> 'User':
        '''
        Find a User by UUID.
        '''
        return cls.query.filter_by(uuid = uuid).first()

    @classmethod
    def find_by_username(cls, username: str) -> 'User':
        '''
        Find a User by username.
        '''
        return cls.query.filter_by(username = username).first()

    @classmethod
    def list_by_role(cls, role: str) -> List['User']:
        '''
        List Users by Role.
        '''
        return cls.query.filter_by(role = role).all()
