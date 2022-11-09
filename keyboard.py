import json


def get_button(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }


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

