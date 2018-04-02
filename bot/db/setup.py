import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine('sqlite:///pob-discord.db', echo=True)

Base = declarative_base()


def init():
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
