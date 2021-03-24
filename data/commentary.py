import datetime
import sqlalchemy
from sqlalchemy import orm
#from .db_session import SqlAlchemyBase
from Class.Application import Application


class Commentary(Application().model):
    __tablename__ = 'commentary'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)
    edited = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))
    quest_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("quests.id"))
    quests = orm.relation("Quest", back_populates='commentary')
    user = orm.relation("User", back_populates='commentary')