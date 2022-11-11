import json


# функция создания организации клавиатуры (кнопок)
def get_button(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }


# функция клавиатуры по старту бота
def get_start_keyboard():
    keyboard = {
        "one_time": True,
        "buttons": [
            [get_button('Начать поиск', 'primary'), get_button('Инфо', 'negative')]
        ]
    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard_info = str(keyboard.decode('utf-8'))
    return keyboard_info


# функция создания кнопки "Начать поиск" после просмотра информации по боту
def button_search():
    keyboard = {
        "one_time": True,
        "buttons": [
            [get_button('Начать поиск', 'primary')]
        ]
    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard_info = str(keyboard.decode('utf-8'))
    return keyboard_info


def button_work():
    keyboard = {
        "one_time": True,
        "buttons": [
            [get_button('Добавить в избранное', 'primary'), get_button('Добавить в черный список', 'negative')],
            [get_button('Удалить из избранного', 'secondary')],
            [get_button('Cледующий', 'positive')]
        ]
    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard_info = str(keyboard.decode('utf-8'))
    return keyboard_info