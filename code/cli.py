'''
Module to add command line functionalities to Flask.
'''
import datetime
from flask.cli import AppGroup
from app.extensions.sqlalchemy import db
from app.entities.user import User
from app.entities.types import RoleType

db_cli = AppGroup('database')

@db_cli.command()
def load():
    '''
    Erase and insert initial data to database.
    '''
    # Erase all data
    User.query.delete()

    # Add the user
    coo = User()
    coo.name = 'Anthony Hopkins'
    coo.position = 'COO'
    coo.birth = datetime.date(year=1937, month=12, day=31)
    coo.username = 'anthony.hopkins'
    coo.password = 'hannibal'

    db.session.add(coo)

    # Add a SysAdmin
    sys_admin = User()
    sys_admin.name = 'Denzel Washington'
    sys_admin.position = 'System Admin'
    sys_admin.role = RoleType.ADMINISTRATOR
    sys_admin.birth = datetime.date(year=1954, month=12, day=28)
    sys_admin.username = 'denzel.washington'
    sys_admin.password = 'trainingday'

    db.session.add(sys_admin)

    db.session.commit()
