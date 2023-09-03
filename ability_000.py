import requests
from urllib.parse import quote
from datetime import datetime
from bs4 import BeautifulSoup
from pytz import timezone
import logging


def parse_tuturu(station_1: str, station_2: str):
    # Определяем URL сайта
    url = f'https://www.tutu.ru/prigorod/search.php?st1={quote(station_1)}&st1_num=&st2={quote(station_2)}&st2_num='
    logging.debug(f"go to url {url}")
    # Отправляем запрос
    response = requests.get(url)

    # Проверяем статус ответа
    if response.status_code != 200:
        logging.debug("not 200 from tutu.ru")
        logging.debug(f"status_code: {response.status_code}")
        logging.debug(f"text: {response.text}")

        return
    else:
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
        logging.debug(f"len1 ({len(elements_from)}), len2 ({len(elements_to)})")
        if len(elements_from) != len(elements_to) or len(elements_from) == 0 or len(elements_to) == 0:
            logging.debug('Произошла ошибка len')
            return

        list_of_tuples = []
        for i in range(len(elements_from)):
            list_of_tuples.append((elements_from[i].text, elements_to[i].text))

        # logging.debug(list_of_tuples)
        return list_of_tuples


def final_response_text(all_today_s_trips, timezone_str):
    # Получение текущего времени
    local_tz = timezone(timezone_str)
    current_time = datetime.now(local_tz).strftime("%H:%M")

    # Поиск индекса элемента, время которого больше текущего
    index = next((i for i, trip in enumerate(all_today_s_trips) if trip[0] > current_time), None)

    if index is not None:
        trips = [[all_today_s_trips[index][0], all_today_s_trips[index][1]]]

        if index + 1 < len(all_today_s_trips):
            trips.append([all_today_s_trips[index + 1][0], all_today_s_trips[index + 1][1]])
        if index + 2 < len(all_today_s_trips):
            trips.append([all_today_s_trips[index + 2][0], all_today_s_trips[index + 2][1]])

        trips_timings = [
            (
                calculate_time_difference(current_time, item[0]),
                calculate_time_difference(item[0], item[1])
            )
            for i, item in enumerate(trips)
        ]

        prefix_templates = [
            "Ближайшее отправление",
            "Второе ближайшее отправление",
            "Третье ближайшее отправление"
        ]

        response_text = ""
        for i in range(len(trips)):
            # Второе ближайшее отправление: через 10 минут в 12:00 с прибытием 13:00, 60 минут в пути.
            line = prefix_templates[i] + ": через " + trips_timings[i][0] + \
                   " минут в " + trips[i][0] + " с прибытием " + trips[i][1] + \
                   ", " + trips_timings[i][1] + " минут в пути. "

            response_text += line

        logging.debug(trips)
        logging.debug(trips_timings)

        return response_text

    # is here if (if index is not None) didn't work
    logging.debug("is here if (if index is not None) didn't work")
    logging.debug("Can't find a trip")
    return


def calculate_time_difference(time1, time2):
    format_str = "%H:%M"
    datetime1 = datetime.strptime(time1, format_str)
    datetime2 = datetime.strptime(time2, format_str)
    time_diff = datetime2 - datetime1
    minutes_diff = time_diff.total_seconds() // 60
    return str(int(minutes_diff))


# LEGACY CODE
class _ScheduleParser:
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
