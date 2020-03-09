from .meta import Engine, DatabasesConnection
from sqlalchemy import Column, String, Integer

Base = Engine()


class User(Base.base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(20), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "username:{};password:{}".format(self.username, self.password)


db_connection = DatabasesConnection(User, Base.engine)
