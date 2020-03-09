import psycopg2
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class Engine:
    def __init__(self, path='postgresql+psycopg2://zhenya:zhenya@localhost/ksis'):
        self.engine = create_engine(path)
        self.base = declarative_base()

    def get_engine_object(self):
        return self.engine

    def create_tables(self):
        self.base.metadata.create_all(self.engine)


class DatabasesConnection:
    def __init__(self, table, engine_connect):
        self.session = sessionmaker(bind=engine_connect)
        self.table = table
