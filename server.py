from config import token, AGE_DELTA, AGEFROM, AGETO
import requests
from datetime import date
from bot import write_message


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
            for i in information_dict:
                self.first_name = i.get('first_name')
                self.city = i.get('city').get('title')
                self.sex = i.get('sex')
                self.bdate = i.get('bdate')
        except KeyError:
            write_message(user_id, 'Извините, техническая проблема, мы занимаемся над ней')

    def get_name(self):
        return self.first_name

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
            'city': self.city,
            'sex': str(sex),
            'age_from': str(age_from),
            'age_to': str(age_to)
        }
