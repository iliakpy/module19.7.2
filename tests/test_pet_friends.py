from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее
    используя этого ключ запрашиваем список всех питомцев и проверяем,
    что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбос', animal_type='шпик',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять
    # запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Шура", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке
    # питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Грюша', animal_type='Котик', age=4):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение
        # с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


    # тест 1
def test_add_new_pet_simple_with_valid_data(name='Кота', animal_type='бенгальская',
                                            age='40'):
    """Проверяем что можно добавить питомца с корректными данными и без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца без фото
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] == ''


    # тест 2
def test_add_photo_of_pet(pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить фото питомца в созданного питомца без фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца без фото
    _, _ = pf.add_new_pet_simple(auth_key, 'КОТ', 'индийский', '8')

    # Запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берем первого питомца (его мы добавили только что) и меняем его фото
    status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

    # Проверяем что статус ответа = 200 и имя питомца не пустое
    assert status == 200
    assert result['pet_photo'] != ''


    # тест 3
def test_add_new_pet_with_invalid_pet_photo(name='Крокодил', animal_type='Шпиц',
                                            age='',
                                            pet_photo=''):
    """Проверяем что нельзя добавить питомца, если не указан путь до файла"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    try:
        _, _ = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        raise Exception("Файл с фотографией питомца существует!")
    except FileNotFoundError:
        print('\nФайл с фотографией питомца или каталог отсутствует!')


    # тест 4
def test_get_api_key_for_invalid_user(email=valid_email, password='66666'):
    """ Проверяем что запрос api ключа возвращает статус 403 при вводе неверного пароля
     и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом
    # статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


    # тест 5
def test_add_new_pet_with_negative_age(name='Кудря', animal_type='турецкий',
                                       age='-5', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца с отрицательным возрастом"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


    # тест 6
def test_add_new_pet_with_invalid_age(name='Василиса', animal_type='египетская',
                                       age='1000', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца с возрастом больше 100 лет"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


    # тест 7
def test_add_new_pet_with_long_name(name='Аваллоннннннннннннннннннннннннннннннннннннннннннн'
                                         'ваапрррррнннннннннннннннннннннннннннннннннннннннн'
                                         'ннннннннннннннннннннннннннннннннннннннннннннннннн'
                                         'ннннннннннн', animal_type='египетская',
                                       age='10', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца с именем длиннее 30 символов"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


    # тест 8
def test_update_pet_info_with_negative_age(name='Мурзик', animal_type='Котфей', age=-5):
    """Проверяем отсутствие возможности обновления информации
       о питомце с отрицательным возрастом"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 400
        assert status == 400
    else:
        # если спиок питомцев пустой, то выкидываем исключение
        # с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

    # тест 9
    def test_update_pet_info_with_long_name(name='Шапооооооооооооооооооооооооооооо'
                                                 'оооооооооооооооооооооооооооооооо'
                                                 'оооооооооооооооооооооооооооооооо'
                                                 'клякаааааааааааааааааааааааааааа'
                                                 'ааа', animal_type='Чебурашка', age=1):
        """Проверяем отсутствие возможности обновления информации о питомце с именем более 30 символов"""

        # Получаем ключ auth_key и список своих питомцев
        _, auth_key = pf.get_api_key (valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets (auth_key, "my_pets")

        # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
        if len (my_pets['pets']) > 0:
            status, result = pf.update_pet_info (auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

            # Проверяем что статус ответа = 400
            assert status == 400
        else:
            # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception ("There is no my pets")

    # тест 10
def test_update_pet_info_with_invalid_age(name='Том', animal_type='Васелиса', age=2000):
    """Проверяем отсутствие возможности обновления информации о питомце с возрастом больше 100 лет"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 400
        assert status == 400
    else:
        # если спиок питомцев пустой, то выкидываем исключение
        # с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


