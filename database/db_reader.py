from database.database import create_session
from database.models import User, FavoriteList, BlackList


class DBReader(object):
    def __init__(self, user_data_dict):
        self.db_session = create_session()
        self.user_data_dict = user_data_dict

    def add_user_to_database(self):
        """ добавляет пользователя в бд """
        user_id = self.user_data_dict['id']
        user_name = self.user_data_dict['name']
        check_user_exist = self.db_session.query(User).filter_by(user_id=user_id).all()

        if not check_user_exist:
            name = user_name
            link = f'vk.com/id{user_id}'
            user = User(user_id=user_id, name=name, link=link)
            self.db_session.add(user)
            self.db_session.commit()
            self.db_session.refresh(user)
            return user.id
        return check_user_exist[0].id

    def add_to_favorite_list(self, friend_info):
        """ добавляет в список избранных """
        user_id = self.add_user_to_database()
        self.db_session.add(FavoriteList(
            favorite_id=friend_info['user_id'],
            name=friend_info['first_name'] + ' ' + friend_info['last_name'],
            bdate=friend_info['user_age'],
            link=f"vk.com/id{friend_info['user_id']}",
            user_id=user_id,
        ))
        self.db_session.commit()

    def add_to_black_list(self, friend_info):
        """ добавляет в список избранных """
        user_id = self.add_user_to_database()
        self.db_session.add(BlackList(
            blacklisted_id=friend_info['user_id'],
            user_id=user_id,
        ))
        self.db_session.commit()
