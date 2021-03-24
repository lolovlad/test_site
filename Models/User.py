import datetime
from sqlalchemy import orm
from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, ForeignKey
from Class.Application import Application
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(Application().model, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    sename = Column(String, nullable=True)
    nickname = Column(String, nullable=True)
    birthday = Column(DateTime, nullable=True)
    icon = Column(LargeBinary, nullable=True)

    email = Column(String, index=True, unique=True, nullable=True)
    phone = Column(Integer, nullable=True)

    type = Column(Integer, default=1)

    hashed_password = Column(String, nullable=True)

    quests = orm.relation("Quest", back_populates='user')
    commentary = orm.relation('Commentary')
    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, val):
        self.hashed_password = generate_password_hash(val)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)



