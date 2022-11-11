import vk_api
from VK_API.vk_class import Vk
from server import UserInfo, UserInfoError
from config import token, TOKEN_VK_USER
from vk_api.longpoll import VkLongPoll, VkEventType
from bot_info import Info, start
from keyboards import get_start_keyboard, button_search

vk = vk_api.VkApi(token=token)
give = vk.get_api()
longpoll = VkLongPoll(vk)


# функция заглушка, в последующем она будет передавать найденные в VK данные пользователю
def search_frends(req):
    return [{
        ''
    }]


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
                    vk = Vk(TOKEN_VK_USER)
                    res = vk.search_for_users_to_meet(user_data_dict) # получаем массив данных пользователей ВК
                    for iter_ in res: # для записи в БД
                        print(iter_)


                    # это я тренируюсь передавать фотографии, в этом формате (часть адресной строки) выдаются сразу фото
                    # write_message(user_id, 'Вот ваши фото', attachment='photo808832_457240640,photo677584128_457240276')
                    # write_message(search_frends(user.get_info()))
                elif message == 'инфо':
                    write_message(user_id, Info.info(), keyboard=button_search())
                else:
                    write_message(user_id, 'я вас не понимаю')


if __name__ == '__main__':
    write_msg()
