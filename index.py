from reactions import *
import logging

logging.getLogger().setLevel(logging.DEBUG)


def handler(event, context):
    logging.debug("start")
    try:
        if 'request' in event and \
                'command' in event['request']:

            logging.debug("command in request; matching...")
            match event['request']['command']:
                case "":
                    return answer_on_init(event, context)
                case "помощь":
                    return answer_on_help(event, context)
                case "что ты умеешь":
                    return answer_on_what(event, context)
                case _:
                    logging.debug("not _ or h or w; searching for st1...")
                    if 'state' in event and \
                            'session' in event['state'] and \
                            'st1' in event['state']['session']:
                        logging.debug("st1 in state")
                        return answer_on_st2(event, context)
                    else:
                        logging.debug("st1 not in state")
                        return answer_on_st1(event, context)

    except Exception as e:
        logging.debug(e)
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': e,
                'end_session': 'true'
            },
        }

    else:
        logging.debug("idk")
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': "idk",
                'end_session': 'true'
            },
        }
