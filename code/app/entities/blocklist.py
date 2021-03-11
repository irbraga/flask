'''
Module with Token Blocklist database mapping.
'''
import datetime
from sqlalchemy import Column, String, DateTime
from app.extensions.sqlalchemy import db

class TokenBlockList(db.Model):
    '''
    Token Blocklist model.
    '''
    __tablename__ = 'tokens_blocklist'

    jti = Column(String, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.now)

    @classmethod
    def is_blocked(cls, jti) -> 'TokenBlockList':
        '''
        Find a Token by JTI.
        '''
        return cls.query.filter_by(jti=jti).first() is not None

    def save(self) -> None:
        '''
        Add the object to the session for persistence.
        '''
        db.session.add(self)
