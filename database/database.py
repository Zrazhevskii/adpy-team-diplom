from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from database.models import create_tables


def create_session():
    dialect = 'postgresql'  # это имя базы данных(mysql, postgresql, mssql, oracle и так далее).
    driver = ''  # используемый DBAPI. Этот параметр является необязательным. Если его
                 # не указать будет использоваться драйвер по умолчанию(если он установлен).
    username = 'postgres'
    password = '1983'  # данные для получения доступа к базе данных.
    host = 'localhost'  # расположение сервера базы данных.
    port = '5432'  # порт для подключения.
    database = 'bot'  # название базы данных.

    DSN = f'{dialect + driver}://{username}:{password}@{host}:{port}/{database}'

    engine = create_engine(DSN)
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
