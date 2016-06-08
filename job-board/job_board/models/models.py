from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    String,
    ForeignKey
)

from .meta import Base


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    company = Column(Text)
    post_date = Column(DateTime)
    description = Column(Text)
    submitter = Column(Integer, ForeignKey("submitter.id"))  #  ,ONDELETE="CASCADE"))

    
class Submitter(Base):
    __tablename__ = 'submitter'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    password = Column(String(128))
