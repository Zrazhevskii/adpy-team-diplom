from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    link = Column(String(length=28), unique=True, nullable=False)

    # удалить
    def __str__(self):
        return f'id: {self.id}, user_id: {self.user_id}, name: {self.name}, link: {self.link}'


class FavoriteList(Base):
    __tablename__ = 'favorite_list'

    id = Column(Integer, primary_key=True)
    favorite_id = Column(Integer, nullable=False)
    name = Column(String(length=40), nullable=False)
    bdate = Column(String(length=8), nullable=False)
    link = Column(String(length=28), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship(User, backref="favorites")


class BlackList(Base):
    __tablename__ = 'black_list'

    id = Column(Integer, primary_key=True)
    blacklisted_id = Column(Integer, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship(User, backref="blacklist")


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
