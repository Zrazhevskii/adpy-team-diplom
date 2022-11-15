import requests
from VK_API.sorting_functions import _sorter_user, _sort_photo_users
from config import TOKEN_VK_USER


class Matchmaking:
    URL = 'https://api.vk.com/method/'

    def __init__(self, token):
        self.params = {'access_token': token, 'v': '5.131'}

    def search_for_users_to_meet(self, dict_):
        """Поиск пользователей по заданным критериям"""
        def_URL = self.URL + 'users.search'
        params_def = {'sex': dict_['sex'],
                      'status': '6',
                      'city': dict_['city'],
                      'age_from': dict_['age_from'],
                      'age_to': dict_['age_to'],
                      'count': '100',
                      'fields': "city, sex, bdate",
                      'has_photo': '1',
                      'sort': '0'
                      }
        req = requests.get(def_URL, params={**self.params, **params_def}).json()
        res = _sorter_user(req['response']['items'], dict_['city'])
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
        if 'error' in req or req['response']['count'] == 0:  # если профиль закрытый или отсутствуют фотографии
            return None
        elif req['response']['count'] != 0:  # если у пользователя в профиле есть фотографии
            res = _sort_photo_users(req['response'])
            return res
