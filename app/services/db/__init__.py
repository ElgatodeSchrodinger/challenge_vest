import os, time

from sqlalchemy import create_engine
from sqlalchemy.orm import close_all_sessions, sessionmaker, registry
from sqlalchemy.engine import url

# Conexión a una base de datos SQL por medio del ORM SQL Alchemy.
# Es agnóstico a la base de datos misma (MySQL, Postgres, etc).

class SQLAlchemyClient():

    def __init__(self):

        pass