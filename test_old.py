import requests
from urllib.parse import quote
from datetime import datetime
from bs4 import BeautifulSoup

station_1_str = "Красный балтиец"
station_2_str = "дмитровская"

# Определяем URL сайта
url = f'https://www.tutu.ru/prigorod/search.php?st1={quote(station_1_str)}&st1_num=&st2={quote(station_2_str)}&st2_num='

# Отправляем запрос
response = requests.get(url)

# Проверяем статус ответа
if response.status_code == 200:
    # Используем библиотеку BeautifulSoup для парсинга HTML
    from lxml import etree

    # Создаем объект BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим нужный элемент на странице
    elements_from = soup.find_all('a', class_='g-link desktop__depTimeLink__1NA_N')

    # Создаем объект BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    elements_to = soup.find_all('a', class_='g-link desktop__arrTimeLink__2TJxM')

    # Выводим найденные элементы
    if len(elements_from) == len(elements_to):
        for i in range(len(elements_from)):
            pass
            #print(elements_from[i].text) #, elements_to[i].text)
    else:
        print('Произошла ошибка len')
        print(len(elements_from))
        print(len(elements_to))

    # Получение текущего времени
    current_time = datetime.now().strftime("%H:%M")

    # Поиск индекса элемента, время которого больше текущего
    index = next((i for i, ts in enumerate(elements_from) if ts.text > current_time), None)

    if index is not None:
        print(elements_from[index].text, elements_to[index].text)
        if index+1 < len(elements_from):
            print(elements_from[index+1].text, elements_to[index+1].text)
        if index+2 < len(elements_from):
            print(elements_from[index+2].text, elements_to[index+2].text)

else:
    print('Произошла ошибка при отправке запроса')
