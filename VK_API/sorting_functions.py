def _sorter_user(list_, city):
    """Сортировка списка пользователей по городу"""
    result_list = []
    for iter_ in list_:
        if iter_.get('city'):  # если пользователь указал город в профиле
            if iter_['city']['id'] == city:
                dict_ = {
                    'user_id': iter_['id'],
                    'first_name': iter_['first_name'],
                    'last_name': iter_['last_name'],
                    'city': iter_['city']['title']
                }
                result_list.append(dict_)
    return result_list


def _sort_photo_users(dict_):
    """Сортировка фотографий пользователя по количеству лайков"""
    if dict_['count'] <= 3:  # если у пользовотеля меньше 3 фотографий получаем имеющиеся
        photo_list = [f"photo{iter_['owner_id']}_{iter_['id']}" for iter_ in dict_['items']]
        return photo_list
    else: # если у пользовотеля больше 3 фотографий получаем имеющиеся
        dict_photo_likes = {f"photo{iter_['owner_id']}_{iter_['id']}": iter_['likes']['count'] for iter_ in
                            dict_["items"]}
        sort_dict_photo_likes = sorted(dict_photo_likes, key=dict_photo_likes.get, reverse=True)[:3]
        return sort_dict_photo_likes


