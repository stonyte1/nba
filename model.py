from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd

engine = create_engine('sqlite:///players_stats.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    first_name = Column('First name', String(30))
    last_name = Column('Surname', String(30))
    height_inches = Column('Height inches', String(10))
    height_feet = Column('Height feet', String(10))

class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    # first_name = Column('First name', String(30))
    # last_name = Column('Surname', String(30))
    pts = Column('Points', Integer)
    reb = Column('Rebound', Integer)
    stl = Column('Steals', Integer)
    player_id = Column('Player', ForeignKey('player.id'))

Base.metadata.create_all(engine)


