from services.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, Float

class BlueQValue(Base):
    __tablename__ = 'blueQValue'
    id = Column(Integer, primary_key=True, autoincrement=True)
    startState = Column(Integer, index=True)
    startEvent = Column(String(255), index=True)
    endEvent = Column(String(255), index=True)
    qValue = Column(Float)
    probability = Column(Float)

class RedQValue(Base):
    __tablename__ = 'redQValue'
    id = Column(Integer, primary_key=True, autoincrement=True)
    startState = Column(Integer, index=True)
    startEvent = Column(String(255), index=True)
    endEvent = Column(String(255), index=True)
    qValue = Column(Float)
    probability = Column(Float)

class Probability(Base):
    __tablename__ = 'probability'
    id = Column(Integer, primary_key=True, autoincrement=True)
    startState = Column(Integer, index=True)
    startEvent = Column(String(255), index=True)
    endEvent = Column(String(255), index=True)
    prob = Column(Float)
    bAdvFar = Column(Float)
    bAdvClose = Column(Float)
    even = Column(Float)
    rAdvClose = Column(Float)
    rAdvFar = Column(Float)

