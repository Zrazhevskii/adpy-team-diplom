import vk_api
from VK_API.vk_class import Matchmaking
from Bot_VK.server import UserInfo, UserInfoError
from config import token, TOKEN_VK_USER
from vk_api.longpoll import VkLongPoll, VkEventType
from bot_info import Info, start
from keyboards import get_start_keyboard, button_search, button_work, start_show
from database.db_reader import DBReader

vk = vk_api.VkApi(token=token)
give = vk.get_api()
longpoll = VkLongPoll(vk)

search_result = []  # список всех пользователей найденных в ВК


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
                    reader = DBReader(user.get_info())
                except UserInfoError as e:
                    write_message(user_id, e)
                    write_message(user_id, 'Попробуйте обратится через несколько минут.')
                    continue
                if message in start:
                    answer = f'Привет, {user.first_name}!\n' \
                             f'Для получения дополнительной информации нажмите "Инфо"\n' \
                             f'Для начала поиска нажмите "Начать поиск"'
                    write_message(user_id, answer, keyboard=get_start_keyboard())
                elif message == 'начать поиск':
                    write_message(user_id, 'Отлично, тогда вперед! Это может занять некоторое время')

                    user_data_dict = user.get_info()
                    vk = Matchmaking(TOKEN_VK_USER)
                    try:
                        res = vk.search_for_users_to_meet(user_data_dict)  # получаем массив данных пользователей ВК
                    except Exception as e:
                        write_message(user_id, 'Попробуйте обратится через несколько минут.')
                        message = ''
                        continue
                    search_result.clear()  # очищаем общий список
                    for iter_ in res:
                        photos = vk.upload_photos(iter_.get('user_id'))
                        if photos:
                            iter_['photos'] = ','.join(photos)
                            search_result.append(iter_)
                    write_message(user_id, 'Найдено записей: {}'.format(len(search_result)), keyboard=start_show())

                elif message == 'инфо':
                    write_message(user_id, Info.info(), keyboard=button_search())
                elif message in ('следующий', 'начать просмотр'):
                    try:
                        friend_info = search_result.pop(0)
                        write_message(user_id, get_user_info_message(friend_info), attachment=friend_info['photos'],
                                      keyboard=button_work())
                    except IndexError:
                        write_message(user_id, 'К сожалению результаты поиска закончились :(')

                elif message == 'добавить в избранное':
                    reader.add_to_favorite_list(friend_info)
                    write_message(user_id, 'Пользователь удачно добавлен в "Избранное"')
                elif message == 'добавить в черный список':
                    reader.add_to_black_list(friend_info)
                    write_message(user_id, 'Пользователь добавлен в "Черный список"')
                elif message == 'показать список избранных':
                    get_all_favorit =                           # вызов всех избранных
                    write_message(user_id, get_all_favorit)
                else:
                    write_message(user_id, 'я вас не понимаю')


if __name__ == '__main__':
    write_msg()
