from services.database import Base
from sqlalchemy import Column, String

class User(Base):
    __tablename__ = 'user'
    id = Column(String(255), primary_key=True)
    username = Column(String(255))
    password = Column(String(255))