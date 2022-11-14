from database import create_session
from models import User, FavoriteList, BlackList
from server import UserInfo
import psycopg2

class db_reader():
    def __init__(self, user_data_dict):
        self.db_session = create_session()
        self.user_data_dict = user_data_dict
        self.

    def _add_user_to_database(self):
        """ добавляет пользователя в бд """
        user_id = self.user_data_dict['id']
        user_name = self.user_data_dict['name']
        check_user_exist = self.db_session.query(User).filter_by(user_id=user_id).all()
        if not check_user_exist:
            name = user_name
            link = f'vk.com/id{user_id}'
            self.db_session.add(User(user_id=user_id, name=name, link=link))
            self.db_session.commit()

    def _check(self):
        q = self.db_session.query(User).all()
        for i in q:
            print(i)
        # print(q)

    def _add_to_favorite_list(self):
        """ добавляет в список избранных """
        self.db_session.add(FavoriteList(favorite_id=, name=, bdate=, link=, user_id=))
        self.db_session.commit()


user_test = UserInfo(user_id=71547447)
xd = db_reader(user_test.get_info())
xd._add_user_to_database()
xd._check()