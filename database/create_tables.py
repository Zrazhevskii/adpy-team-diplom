from database import get_engine, DSN
from models import create_tables


create_tables(get_engine(DSN))
