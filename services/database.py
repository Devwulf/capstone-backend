from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

file_path = os.path.abspath(os.getcwd())+"/db/database.db"
engine = create_engine('sqlite:///' + file_path)
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
    import api.model.dbModels
    Base.metadata.create_all(bind=engine)

def init_model_db():
    print("Setting up the trained model database...")

    from api.model.dbModels import BlueQValue, RedQValue, Probability
    import pandas as pd
    blueMdp = pd.read_pickle("static/blueTrained.pkl")
    redMdp = pd.read_pickle("static/redTrained.pkl")
    goldAdv = pd.read_pickle("static/eventsGoldAdvMdp.pkl")
    pairedEvents = pd.read_pickle("static/pairedEventsDf.pkl")
    pairedEvents = pairedEvents[pairedEvents["StartState"] == 0]
    mdp = pd.read_pickle("static/mdpDf.pkl")
    
    # Processes the pre-trained model for the Blue team
    if BlueQValue.query.first() is None:
        # Fill with data from pickle
        for row in blueMdp.itertuples():
            db_session.add(BlueQValue(startState=row.StartState, 
                                      startEvent=row.StartEvent, 
                                      endEvent=row.EndEvent, 
                                      qValue=row.QValues,
                                      probability=row.Probability))
        db_session.commit()

    # Processes the pre-trained model for the Red team
    if RedQValue.query.first() is None:
        for row in redMdp.itertuples():
            db_session.add(RedQValue(startState=row.StartState, 
                                     startEvent=row.StartEvent, 
                                     endEvent=row.EndEvent, 
                                     qValue=row.QValues,
                                     probability=row.Probability))
        db_session.commit()

    if Probability.query.first() is None:
        # First few rows show the starting probabilities of the actions
        for action in goldAdv[goldAdv["StartState"] == 0]["StartEvent"].unique():
            prob = len(pairedEvents[pairedEvents["StartEvent"] == action]) / len(pairedEvents)
            db_session.add(Probability(startState=-1, endEvent=action, prob=prob))

        # These are the rest of the probabilities of the actions
        for i in range(len(goldAdv)):
            goldRow = goldAdv.iloc[i]
            probRow = mdp.iloc[i]
            db_session.add(Probability(startState=goldRow.StartState, 
                                       startEvent=goldRow.StartEvent, 
                                       endEvent=goldRow.EndEvent, 
                                       prob=probRow.Probability, 
                                       bAdvFar=goldRow.bAdvFar, 
                                       bAdvClose=goldRow.bAdvClose, 
                                       even=goldRow.Even, 
                                       rAdvClose=goldRow.rAdvClose, 
                                       rAdvFar=goldRow.rAdvFar))
        db_session.commit()

    print("Finished setting up the trained model database!")

def init_auth():
    from auth.models.models import User
    from werkzeug.security import generate_password_hash
    import uuid
    if User.query.first() is None:
        db_session.add(User(id=str(uuid.uuid4()), 
                            username="test", 
                            password=generate_password_hash("test123", method="sha256")))
        db_session.commit()

