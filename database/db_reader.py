from sqlalchemy import and_

from database.database import create_session
from database.models import User, FavoriteList, BlackList
from sqlalchemy.sql import exists


class DBReader(object):
    def __init__(self, user_data_dict):
        self.db_session = create_session()
        self.user_id = user_data_dict['id']
        self.user_name = user_data_dict['name']

    def add_user_to_database(self):
        """ добавляет пользователя в бд """
        check_user_exist = self.db_session.query(User).filter_by(user_id=self.user_id).all()
        if not check_user_exist:
            name = self.user_name
            link = f'vk.com/id{self.user_id}'
            self.db_session.add(User(user_id=self.user_id, name=name, link=link))
            self.db_session.commit()

    def add_to_favorite_list(self, friend_info):
        """ добавляет в список избранных """
        self.db_session.add(FavoriteList(
            favorite_id=friend_info['user_id'],
            name=f"{friend_info['first_name']} {friend_info['last_name']}",
            bdate=friend_info['user_age'],
            link=f"vk.com/id{friend_info['user_id']}",
            user_id=self.user_id
        ))
        self.db_session.commit()

    def add_to_black_list(self, friend_info):
        """ Добавляет в черный список """
        self.db_session.add(BlackList(
            blacklisted_id=friend_info['user_id'],
            user_id=self.user_id
        ))
        self.db_session.commit()

    def get_favorite_list(self):
        """ получить список избранных """
        favorite_list = []
        favorite_list_ = self.db_session.query(FavoriteList).filter_by(user_id=self.user_id).all()

        for favorite in favorite_list_:
            favorite_list.append(favorite)
        return favorite_list

    def get_black_list(self, id_):
        """Метод проверяет наличие id найденных пользователей в черном списке"""
        black_list = self.db_session.query(
            exists().where(and_(BlackList.blacklisted_id == id_, BlackList.user_id == self.user_id))).scalar()
        return black_list
