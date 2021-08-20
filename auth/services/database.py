from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool

engine = create_engine('sqlite://',
                        convert_unicode=True,
                        connect_args={"check_same_thread": False}, # only for in-memory databases
                        poolclass=StaticPool) # only for in-memory databases
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import auth.models.models
    Base.metadata.create_all(bind=engine)