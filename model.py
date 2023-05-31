from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///players_stats.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    first_name = Column('First name', String(30))
    last_name = Column('Surname', String(30))
    pts = Column('Points', Integer)
    reb = Column('Rebound', Integer)
    stl = Column('Steals', Integer)

Base.metadata.create_all(engine)
