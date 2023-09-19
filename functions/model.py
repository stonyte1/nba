from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///nba_stats.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    first_name = Column('first_name', String(30))
    last_name = Column('surname', String(30))
    height_inches = Column('height_inches', String(10))
    height_feet = Column('height_feet', String(10))

class Game(Base):
    __tablename__ = 'season_games'
    id = Column(Integer, primary_key=True)
    pts = Column('points', Integer)
    reb = Column('rebound', Integer)
    stl = Column('steals', Integer)
    date = Column('date', String(30))
    game_id = Column('game_id', Integer)
    team = Column('team', String(30))
    player_id = Column('player_id', ForeignKey('player.id'))
