from datetime import datetime


def calculation_time(call_function):

    def wrapper(*args, **named_arguments):
        start_datetime = datetime.now()
        result = call_function(*args, **named_arguments)
        print('function', call_function.__name__, 'time:', datetime.now() - start_datetime)
        return result

    return wrapper
