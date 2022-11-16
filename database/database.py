from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from local_cofig import db_name, password

DSN = f"postgresql://postgres:{password}@localhost:5432/{db_name}"


def get_engine(DSN):
    return create_engine(DSN)


def create_session():
    engine = get_engine(DSN)
    # create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
