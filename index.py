from ability_000 import ScheduleParser


def handler(event, context):
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """

    try:
        if 'session' in event and 'message_id' in event['session']:

            match event['session']['message_id']:
                # Назовите Станцию Отправления
                case 0:

                    text = 'Назовите Станцию Отправления:'
                    end_session = 'false'
                    session_dict = None

                # Назовите Станцию Прибытия
                case 1:

                    if 'request' in event and \
                            'original_utterance' in event['request'] \
                            and len(event['request']['original_utterance']) > 0:

                        text = 'Назовите Станцию Прибытия:'
                        end_session = 'false'
                        session_dict = {'st1': event['request']['original_utterance']}

                # Возврат расписания
                case 2:

                    if 'request' in event and \
                            'original_utterance' in event['request'] \
                            and len(event['request']['original_utterance']) > 0:

                        if 'state' in event and \
                                'session' in event['state'] and \
                                'st1' in event['state']['session']:
                            st1 = event['state']['session']['st1']
                        else:
                            raise 'State error'

                        st2 = event['request']['original_utterance']

                        try:
                            schedule = ScheduleParser(str(st1), str(st2)).parse()

                            if schedule["error"] is None:
                                text = 'Ближайшее отправление: ' + schedule['r1'][0] + ' с прибытием ' + schedule['r1'][1] + \
                                       '. Второе ближайшее отправление: ' + schedule['r2'][0] + ' с прибытием ' + schedule['r2'][1] + \
                                       '. Третье ближайшее отправление: ' + schedule['r3'][0] + ' с прибытием ' + schedule['r3'][1]
                                end_session = 'true'
                                session_dict = None
                            else:
                                text = schedule['error']
                                end_session = 'true'
                                session_dict = None
                        except Exception as e:
                            text = str(e)
                            end_session = 'true'
                            session_dict = None

    except Exception as e:
        text = str(e)
        end_session = 'true'
        session_dict = None

    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            # Respond with the original request or welcome the user if this is the beginning of the dialog and the request has not yet been made.
            'text': text,
            # Don't finish the session after this response.
            'end_session': end_session
        },
        'session_state': session_dict
    }
