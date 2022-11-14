from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import create_tables


def create_session():
    # DSN = "postgresql://postgres:PASS@localhost:5432/NAME"
    engine = create_engine(DSN)
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
