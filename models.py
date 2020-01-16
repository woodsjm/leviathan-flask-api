from peewee import *
from flask_login import UserMixin
import datetime

import os

from playhouse.db_url import connect

DATABASE = SqliteDatabase('leviathan.sqlite')

#User Model
class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User])
    print("TABLES CREATED")
    DATABASE.close()