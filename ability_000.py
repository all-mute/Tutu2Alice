import requests
from urllib.parse import quote
from datetime import datetime
from bs4 import BeautifulSoup
from pytz import timezone


class ScheduleParser:
    def __init__(self, station_1, station_2):
        self.station_1 = station_1
        self.station_2 = station_2

    def parse(self):
        result_dict = {
            'r1': [],
            'r2': [],
            'r3': [],
            'error': None,
        }


        # Определяем URL сайта
        url = f'https://www.tutu.ru/prigorod/search.php?st1={quote(self.station_1)}&st1_num=&st2={quote(self.station_2)}&st2_num='

        # Отправляем запрос
        response = requests.get(url)

        # Проверяем статус ответа
        if response.status_code == 200:
            # Используем библиотеку BeautifulSoup для парсинга HTML

            # Создаем объект BeautifulSoup
            # Находим нужный элемент на странице
            soup = BeautifulSoup(response.text, 'html.parser')
            elements_from = soup.find_all('a', class_='g-link desktop__depTimeLink__1NA_N')

            # Создаем объект BeautifulSoup
            # Находим нужный элемент на странице
            soup = BeautifulSoup(response.text, 'html.parser')
            elements_to = soup.find_all('a', class_='g-link desktop__arrTimeLink__2TJxM')

            # Выводим найденные элементы
            if len(elements_from) != len(elements_to) or len(elements_from) == 0 or len(elements_to) == 0:
                result_dict['error'] = f'Произошла ошибка len1 ({len(elements_from)}) != len2 ({len(elements_to)})'
                return result_dict

            # Получение текущего времени
            moscow_tz = timezone('Europe/Moscow')
            current_time = datetime.now(moscow_tz).strftime("%H:%M")

            # Поиск индекса элемента, время которого больше текущего
            index = next((i for i, ts in enumerate(elements_from) if ts.text > current_time), None)

            if index is not None:
                result_dict['r1'] = [elements_from[index].text, elements_to[index].text]
                if index + 1 < len(elements_from):
                    result_dict['r2'] = [elements_from[index + 1].text, elements_to[index + 1].text]
                if index + 2 < len(elements_from):
                    result_dict['r3'] = [elements_from[index + 2].text, elements_to[index + 2].text]

                return result_dict
            else:
                result_dict['error'] = 'Произошла ошибка: Поиск индекса элемента, время которого больше текущего'
                return result_dict
