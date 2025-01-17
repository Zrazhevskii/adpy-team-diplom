from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.models import create_tables


def create_session():
    DSN = f"postgresql://postgres:PASS@localhost:5432/NAME"
    engine = create_engine(DSN)
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
