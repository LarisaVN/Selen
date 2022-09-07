#!/usr/bin/python3
# -*- encoding=utf8 -*-

# You can find very simple example of the usage Selenium with PyTest in this file.
#
# More info about pytest-selenium:
#    https://pytest-selenium.readthedocs.io/en/latest/user_guide.html
#
# How to run:
#  1) Download geko driver for Chrome here:
#     https://chromedriver.storage.googleapis.com/index.html?path=2.43/
#  2) Install all requirements:
#     pip install -r requirements.txt
#  3) Run tests:
#     python3 -m pytest -v --driver Chrome --driver-path /tests/chrome test_selenium_simple.py
#
import pytest
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")

driver = webdriver.Chrome(executable_path="c:\ch_drv\chromedriver.exe", chrome_options=chrome_options)

# Базовый класс исключений для этого проекта
class APIException(Exception):
     pass

#@pytest.fixture(autouse=True)
@pytest.fixture
def testing():
    #driver = webdriver.Chrome(executable_path="c:\ch_drv\chromedriver.exe", chrome_options=chrome_options)

    # Open PetFriends base page:
    driver.get("https://petfriends.skillfactory.ru//")

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-success")))

    # Find the field for search text input:
    btn_newuser = driver.find_element_by_xpath("//button[@onclick=\"document.location='/new_user';\"]")
    btn_newuser.click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "У меня уже есть аккаунт")))

    btn_exist_acc = driver.find_element_by_link_text(u"У меня уже есть аккаунт")
    btn_exist_acc.click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "Зарегистрироваться")))

    field_email = driver.find_element_by_id("email")
    field_email.click()
    field_email.clear()
    field_email.send_keys("lnch_16@rambler.ru")

    field_pass = driver.find_element_by_id("pass")
    field_pass.click()
    field_pass.clear()
    field_pass.send_keys("LarisaN22")

    btn_submit = driver.find_element_by_xpath("//button[@type='submit']")
    btn_submit.click()

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card")))

    btn_exist_acc = driver.find_element_by_link_text(u"Мои питомцы")
    btn_exist_acc.click()
    yield

@pytest.mark.nondestructive
def test_all_pets_present():

    driver.quit()

    drv = webdriver.Chrome(executable_path="c:\ch_drv\chromedriver.exe", chrome_options=chrome_options)

    drv.implicitly_wait(15)

    # Open PetFriends base page:
    drv.get("https://petfriends.skillfactory.ru//");

    #WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-success")))

    # Find the field for search text input:
    btn_newuser = drv.find_element_by_xpath("//button[@onclick=\"document.location='/new_user';\"]")
    btn_newuser.click()

    #WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "У меня уже есть аккаунт")))

    btn_exist_acc = drv.find_element_by_link_text(u"У меня уже есть аккаунт")
    btn_exist_acc.click()

    #WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "Зарегистрироваться")))

    field_email = drv.find_element_by_id("email")
    field_email.click()
    field_email.clear()
    field_email.send_keys("lnch_16@rambler.ru")

    field_pass = drv.find_element_by_id("pass")
    field_pass.click()
    field_pass.clear()
    field_pass.send_keys("LarisaN22")
    
    btn_submit = drv.find_element_by_xpath("//button[@type='submit']")
    btn_submit.click()

    #WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card")))

    btn_exist_acc = drv.find_element_by_link_text(u"Мои питомцы")
    btn_exist_acc.click()

    #WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))

    # Выбираем все строки тела таблицы (без заголовка)
    tables_body = drv.find_elements_by_tag_name("tbody")
    my_strings = tables_body[0].find_elements_by_tag_name("tr")
    # Вычисляем количество питомцев в таблице
    str_num = len(my_strings)

    # Получаем строку со всей статистикой
    statistic = drv.find_element_by_class_name("\\.col-sm-4.left")
    stat_strings = statistic.text.split()
    tmp_len = len(stat_strings)

    # Заводим и инициализируем переменную под количество питомцев из статистики
    pet_num = -1

    # Извлекаем количество питомцев из статистики
    for i in range(tmp_len):
        if (stat_strings[i] == "Питомцев:" and i < (tmp_len - 1)):
            try:
                pet_num = int(stat_strings[i + 1])
            except:
                raise APIException('Ошибка преобразования в целое')
            break

    drv.quit()

    assert pet_num > 0, 'Нет количества питомцев в статистике'
    assert str_num == pet_num, 'Ошибка в количестве питомцев '


@pytest.mark.nondestructive
def test_pets_photos(testing):

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))

    # Выбираем все строки тела таблицы (без заголовка)
    tables_body = driver.find_elements_by_tag_name("tbody")
    my_str_photos = tables_body[0].find_elements_by_tag_name("img")
    # Вычисляем количество питомцев в таблице
    str_num = len(my_str_photos)

    # Получаем строку со всей статистикой
    statistic = driver.find_element_by_class_name("\\.col-sm-4.left")
    stat_strings = statistic.text.split()
    tmp_len = len(stat_strings)

    # Заводим и инициализируем переменную под количество питомцев из статистики
    pet_num = -1

    # Извлекаем количество питомцев из статистики
    for i in range(tmp_len):
        if (stat_strings[i] == "Питомцев:" and i < (tmp_len - 1)):
            try:
                pet_num = int(stat_strings[i + 1])
            except:
                raise APIException('Ошибка преобразования в целое')
            break

    # Разбираем строки таблицы с питомцами

    # Заводим и инициализируем переменную под количество фотографий
    photo_num = 0

    for i in range(str_num):
        if (my_str_photos[i].get_attribute('src') != ''):
            photo_num += 1

    driver.quit()

    # Ровно половина от статистики (вообще, находится под проверкой)!
    half_num = float(pet_num)/2

    assert pet_num > 0, 'Нет количества питомцев в статистике'
    assert half_num <= photo_num, 'Мало фотографий'

@pytest.mark.nondestructive
def test_pets_parametrs(testing):

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "td")))

    # Выбираем все строки тела таблицы (без заголовка)
    tables_body = driver.find_elements_by_tag_name("tbody")
    my_str_descriptions = tables_body[0].find_elements_by_tag_name("td")
    #Количество ячеек с данными в таблице
    cell_num = len(my_str_descriptions)

    # Получаем строку со всей статистикой
    statistic = driver.find_element_by_class_name("\\.col-sm-4.left")
    stat_strings = statistic.text.split()
    tmp_len = len(stat_strings)

    # Заводим и инициализируем переменную под количество питомцев из статистики
    pet_num = -1

    # Извлекаем количество питомцев из статистики
    for i in range(tmp_len):
        if (stat_strings[i] == "Питомцев:" and i < (tmp_len - 1)):
            try:
                pet_num = int(stat_strings[i + 1])
            except:
                raise APIException('Ошибка преобразования в целое')
            break

    # Разбираем строки таблицы с питомцами

    # Заводим и инициализируем переменную под количество питомцев со всеми параметрами
    descriptions_num = 0

    for str_idx in range(0, cell_num, 4):
        if (my_str_descriptions[str_idx].text != '' and my_str_descriptions[str_idx + 1].text != '' and my_str_descriptions[str_idx + 2].text != ''):
            descriptions_num += 1

    driver.quit()

    assert pet_num > 0, 'Нет количества питомцев в статистике'
    assert pet_num == descriptions_num, 'Есть питомцы с пробелами в биографии'

@pytest.mark.nondestructive
def test_pets_unique_name(testing):

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "td")))

    # Выбираем все строки тела таблицы (без заголовка)
    tables_body = driver.find_elements_by_tag_name("tbody")
    my_str_descriptions = tables_body[0].find_elements_by_tag_name("td")
    #Количество ячеек с данными в таблице
    cell_num = len(my_str_descriptions)


    # Разбираем строки таблицы с питомцами
    names_of_pets = []

    for str_idx in range(0, cell_num, 4):
        names_of_pets.append(my_str_descriptions[str_idx].text)

    driver.quit()

    #Проверяем уникальность имен
    unique_flag = 1
    num_pet = names_of_pets.__len__()

    for i in range(num_pet):
       if(names_of_pets.count(names_of_pets[i]) > 1):
           unique_flag = 0
           break

    assert unique_flag != 0, 'Есть питомцы с совпадающими именами'

@pytest.mark.nondestructive
def test_pets_unique_pet(testing):

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "td")))

    # Выбираем все строки тела таблицы (без заголовка)
    tables_body = driver.find_elements_by_tag_name("tbody")
    my_str_descriptions = tables_body[0].find_elements_by_tag_name("td")
    #Количество ячеек с данными в таблице
    cell_num = len(my_str_descriptions)

    # Разбираем строки таблицы с питомцами
    names_of_pets = []

    for str_idx in range(0, cell_num, 4):
        combo_str = my_str_descriptions[str_idx].text + ' ' + my_str_descriptions[str_idx + 1].text  + ' ' + my_str_descriptions[str_idx + 2].text
        names_of_pets.append(combo_str)

    driver.quit()

    #Проверяем уникальность имен
    unique_flag = 1
    num_pet = names_of_pets.__len__()

    for i in range(num_pet):
       if(names_of_pets.count(names_of_pets[i]) > 1):
           unique_flag = 0
           break

    assert unique_flag != 0, 'Есть одинаковые питомцы'