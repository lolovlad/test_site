import datetime
import sqlalchemy
from sqlalchemy import orm
#from .db_session import SqlAlchemyBase
from Class.Application import Application


class Quest(Application().model):
    __tablename__ = 'quests'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    likes = sqlalchemy.Column(sqlalchemy.Integer,
                              default=0)
    dislikes = sqlalchemy.Column(sqlalchemy.Integer,
                              default=0)
    views = sqlalchemy.Column(sqlalchemy.Integer,
                              default=0)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    commentary = orm.relation('Commentary')