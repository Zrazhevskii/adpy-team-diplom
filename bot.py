import vk_api
from server import UserInfo
from config import token
from vk_api.longpoll import VkLongPoll, VkEventType
from bot_info import Info
from keyboard import get_start_keyboard, button_search

vk = vk_api.VkApi(token=token)
give = vk.get_api()
longpoll = VkLongPoll(vk)


# Функция написания сообщений, клавиатура = None, потому что клавиатуры может быть и не быть
def write_message(user_id, text, keyboard=None):
    post = {
        'user_id': user_id,
        'message': text,
        'random_id': 0,
        'keyboard': keyboard
    }
    vk.method('messages.send', post)


# функция отслеживает поступающие от пользователя сообщения
def write_msg():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                message = event.text.lower()
                user_id = event.user_id
                user = UserInfo(user_id)
                name = user.get_name()
                print(user.get_info())
                if message == 'начать':
                    answer = f'Привет, {name}!\n' \
                             f'Для получения дополнительной информации нажмите "Инфо"\n' \
                             f'Для начала поиска нажмите "Начать поиск"'
                    # В функции передаем кнопки "Инфо", "Начать поиск"
                    write_message(user_id, answer, keyboard=get_start_keyboard())
                elif message == 'начать поиск':
                    write_message(user_id, 'Отлично, тогда вперед')

                elif message == 'инфо':
                    write_message(user_id, Info.info(), keyboard=button_search())
                else:
                    write_message(user_id, 'Я вас не понимаю :(')


if __name__ == '__main__':
    write_msg()
