from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.models import create_tables


def create_session():
    DSN = f"postgresql://postgres:r3l0ATprogef3w_+@localhost:5432/adv_dip"
    engine = create_engine(DSN)
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
