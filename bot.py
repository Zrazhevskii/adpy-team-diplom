import vk_api

from VK_API.vk_class import Matchmaking
from database.db_reader import Db_reader
from server import UserInfo, UserInfoError
from config import token, TOKEN_VK_USER
from vk_api.longpoll import VkLongPoll, VkEventType
from bot_info import Info, start
from keyboards import get_start_keyboard, button_search, button_work, start_show

vk = vk_api.VkApi(token=token)
give = vk.get_api()
longpoll = VkLongPoll(vk)

search_result = [] # список всех пользователей найденных в ВК


# функция вывода пользователю полученной в ВК информации
def get_user_info_message(user_info):
    return '{} {}\n{}'.format(
        user_info.get('first_name'),
        user_info.get('last_name'),
        'https://vk.com/id{}'.format(user_info.get('user_id')),
    )


# Функция написания сообщений пользователю
def write_message(user_id, text, keyboard=None, attachment=None):
    post = {
        'user_id': user_id,
        'message': text,
        'random_id': 0,
        'keyboard': keyboard,
        'attachment': attachment
    }
    vk.method('messages.send', post)


# функция отслеживает поступающие от пользователя сообщения
def write_msg():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                message = event.text.lower()
                user_id = event.user_id
                try:
                    user = UserInfo(user_id)
                except UserInfoError as e:
                    write_message(user_id, e)
                    write_message(user_id, 'Попробуйте обратится через несколько минут.')
                    continue
                name = user.get_name()
                if message in start:
                    answer = f'Привет, {name}!\n' \
                             f'Для получения дополнительной информации нажмите "Инфо"\n' \
                             f'Для начала поиска нажмите "Начать поиск"'
                    write_message(user_id, answer, keyboard=get_start_keyboard())
                elif message == 'начать поиск':
                    write_message(user_id, 'Отлично, тогда вперед!')
                    user_data_dict = user.get_info()
                    xd = Db_reader(user_data_dict)
                    xd._add_user_to_database() # записываем пользователя в БД
                    matchmaking = Matchmaking(TOKEN_VK_USER)
                    try:
                        res = matchmaking.search_for_users_to_meet(user_data_dict) # получаем данные пользователей ВК
                    except Exception as e:
                        write_message(user_id, 'Попробуйте обратится через несколько минут.')
                        message = ''
                        continue
                    search_result.clear() # очищаем общий список
                    for iter_ in res:
                        photos = matchmaking.upload_photos(iter_.get('user_id'))
                        if photos:
                            iter_['photos'] = ''.join(photos)
                            search_result.append(iter_)
                    write_message(user_id, f'Найдено записей: {len(search_result)}', keyboard=start_show())

                elif message in ('следующий', 'начать просмотр', 'Добавить в избранное'):
                    user_info = search_result.pop(0)
                    write_message(user_id, get_user_info_message(user_info), attachment=user_info['photos'],
                                  keyboard=button_work())
                else:
                    write_message(user_id, 'я вас не понимаю')


if __name__ == '__main__':
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                message = event.text.lower()
                user_id = event.user_id
                try:
                    user = UserInfo(user_id)
                except UserInfoError as e:
                    write_message(user_id, e)
                    write_message(user_id, 'Попробуйте обратится через несколько минут.')
                    continue
                name = user.get_name()
                if message in start:
                    answer = f'Привет, {name}!\n' \
                             f'Для получения дополнительной информации нажмите "Инфо"\n' \
                             f'Для начала поиска нажмите "Начать поиск"'
                    write_message(user_id, answer, keyboard=get_start_keyboard())
                elif message == 'начать поиск':
                    write_message(user_id, 'Отлично, тогда вперед!')
                    user_data_dict = user.get_info()
                    xd = Db_reader(user_data_dict)
                    xd._add_user_to_database() # записываем пользователя в БД
                    matchmaking = Matchmaking(TOKEN_VK_USER)
                    try:
                        res = matchmaking.search_for_users_to_meet(user_data_dict) # получаем данные пользователей ВК
                    except Exception as e:
                        write_message(user_id, 'Попробуйте обратится через несколько минут.')
                        message = ''
                        continue
                    search_result.clear() # очищаем общий список
                    for iter_ in res:
                        photos = matchmaking.upload_photos(iter_.get('user_id'))
                        if photos:
                            iter_['photos'] = ''.join(photos)
                            search_result.append(iter_)
                    write_message(user_id, f'Найдено записей: {len(search_result)}', keyboard=start_show())

                elif message in ('следующий', 'начать просмотр', 'Добавить в избранное'):
                    user_info = search_result.pop(0)
                    write_message(user_id, get_user_info_message(user_info), attachment=user_info['photos'],
                                  keyboard=button_work())
                else:
                    write_message(user_id, 'я вас не понимаю')

