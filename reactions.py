from ability_000 import parse_tuturu, final_response_text
import logging


def answer_on_init(event, context):
    text = "Здравствуйте, это навык для получения расписания отхода ближайших электричек. Назовите станцию отправления:"

    logging.debug(text)
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': 'false'
        },
    }


def answer_on_help(event, context):
    text = """С помощью этого навыка можно узнать расписание отхода ближайших электричек. Сначала навык узнает у вас станцию отправления, затем станцию прибытия.
    Примеры названий станций: Москва, Москва-Ярославская, Красный балтиец.
    Текущее время определяется автоматически, в зависимости от часового пояса вашего устройства.
    После ответа с расписанием навык прекращает работу.
    Вы можете назвать станцию отправления прямо сейчас:"""

    logging.debug(text)
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': 'false'
        },
    }


def answer_on_what(event, context):
    text = """С помощью этого навыка можно узнать расписание отхода ближайших электричек. Сначала навык узнает у вас станцию отправления, затем станцию прибытия.
        Примеры названий станций: Москва, Москва-Ярославская, Красный балтиец.
        Текущее время определяется автоматически, в зависимости от часового пояса вашего устройства.
        После ответа с расписанием навык прекращает работу.
        Вы можете назвать станцию отправления прямо сейчас:"""

    logging.debug(text)
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': 'false'
        },
    }


def answer_on_st1(event, context):
    text = "Назовите станцию прибытия:"
    st1 = event['request']['command']

    logging.debug(text)
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': 'false'
        },
        'session_state': {'st1': st1}
    }


def answer_on_st2(event, context):
    st1 = event['state']['session']['st1']
    st2 = event['request']['command']
    local_tz = event["meta"]["timezone"]

    text = final_response_text(parse_tuturu(st1, st2), local_tz)

    logging.debug(text)
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': 'true'
        },
    }
