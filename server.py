from config import token, AGE_DELTA, AGEFROM, AGETO
import requests
from datetime import date


# класс обрабатывающий ошибку при получении пустого 'response'
# и исключения циклического импорта
class UserInfoError(Exception):
    pass


# Класс для работы с ВК для обработки информации по текущему пользователю
# работающему с ботом и передаче информации для поиска пользователей для знакомства
class UserInfo:
    def __init__(self, user_id):
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': token,
                  'user_ids': user_id,
                  'fields': 'city, sex, bdate',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_dict = response['response']
        except KeyError:
            print('Хьюстон, у нас технические проблемы!')
            raise UserInfoError('Извините, техническая проблема, мы занимаемся над ней')
        for i in information_dict:
            city = i.get('city')
            if city:
                self.city = city["id"]
            else:
                self.city = ''
            self.sex = i.get('sex')
            self.user_id = i.get('id')
            self.bdate = i.get('bdate')
            self.first_name = i.get('first_name')
            self.last_name = i.get('last_name')

    # функция для извлечения имени, отдельно для облегчения и более уважительного обращения к пользователю
    def get_name(self):
        return self.first_name

    # функция для передачи информации в модуль работы с ВК для поиска знакомств
    def get_info(self):
        if self.bdate:
            _, _, year = self.bdate.split('.')
            age = date.today().year - int(year)
            age_from = age - AGE_DELTA
            age_to = age + AGE_DELTA
        else:
            age_from = AGEFROM
            age_to = AGETO
        if self.sex:
            sex = 1 if self.sex == 2 else 2
        else:
            sex = 0
        return {
            'id': self.user_id,
            'city': self.city,
            'sex': str(sex),
            'age_from': str(age_from),
            'age_to': str(age_to),
            'name': f'{self.first_name} {self.last_name}'
        }
