import datetime
from sqlalchemy import Column, Integer, String, LargeBinary
from Class.Application import Application


class Sound(Application().model):
    __tablename__ = "sounds"

    id = Column(Integer, primary_key=True)
    name = Column(String)

