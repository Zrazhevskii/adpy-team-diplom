import requests
from VK_API.sorting_functions import _sorter_user, _sort_photo_users
from config import TOKEN_VK_USER

class Vk:
    URL = 'https://api.vk.com/method/'

    def __init__(self, token):
        self.params = {'access_token': token, 'v': '5.131'}

    def search_for_users_to_meet(self, dict_, offset=0):
        """Поиск пользователей по заданным критериям"""
        def_URL = self.URL + 'users.search'
        list_user = []
        flag = 0
        params_def = {'sex': dict_['sex'],
                      'status': '6',
                      'city': dict_['city'],
                      'offset': offset,
                      'age_from': dict_['age_from'],
                      'age_to': dict_['age_to'],
                      'count': '1000',
                      'fields': "city, sex",
                      'has_photo': '1',
                      'sort': '0'
                      }
        while True: # запускаем цикл для формирования списка пользователей
            req = requests.get(def_URL, params={**self.params, **params_def}).json()
            result = req['response']
            offset += result['count'] # если количество пользователей больше увеличиваем offset
            list_user.extend(req['response']['items']) # добавляем к списку полученных пользователей
            if flag == result['count']: # если флаг равен количесту всех выгруженных пользователей прерываем цикл
                break
            else:
                flag += result['count'] # если флаг равен количесту всех выгруженных цикл продолжаем
        res = _sorter_user(list_user, dict_['city'])
        return res

    def upload_photos(self, id_user):
        """Функция находит фотографии в профиле пользователя по id и возвращает список в формате photoХХХХ_УУУУ"""
        def_URL = self.URL + "photos.get"
        params_def = {
            'owner_id': id_user,
            'album_id': 'profile',
            'extended': '1',
        }
        req = requests.get(def_URL, params={**self.params, **params_def}).json()
        # time.sleep(0.34)
        if 'error' in req: # если профиль закрытый
            return 'Профиль приватный'
        elif req['response']['count'] == 0: # если у пользователя в профиле отсутствуют фотографии
            return 'У пользователя нет фотографий'
        elif req['response']['count'] != 0: # если у пользователя в профиле есть фотографии
            res = _sort_photo_users(req['response'])
            return res


