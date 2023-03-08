# tested
import math
import api.common.message as acm


def get_log_value(number, base_number=math.e):  # tested
    log_value = get_math_nan_value()
    try:
        if number > 0:
            log_value = math.log(number, base_number)
    except:
        acm.show_exception_message('Having unexpected error for log calculation [' + str(number) + ', ' + str(base_number) + '], and return nan value.')
    return log_value


def get_exponential_value(number, base_number=math.e):  # tested
    exponential_value = get_math_nan_value()
    try:
        exponential_value = math.pow(base_number, number)
    except:
        acm.show_exception_message('Having unexpected error for power calculation [' + str(number) + ', ' + str(base_number) + '], and return nan value.')
    return exponential_value


def get_updated_max(current_max, new_value):  # tested
    try:
        if current_max > new_value:
            return current_max
        else:
            return new_value
    except:
        print('Having unexpected error to get max[' + str(current_max) + ', ' + str(new_value) + '], and return None value.')
        return get_math_nan_value()


def get_updated_min(current_min, new_value):  # tested
    try:
        if current_min < new_value:
            return current_min
        else:
            return new_value
    except:
        print('Having unexpected error to get min[' + str(current_min) + ', ' + str(new_value) + '], and return None value.')
        return get_math_nan_value()


def check_whether_nan_value(number):  # tested
    try:
        return math.isnan(number)
    except:
        acm.show_exception_message('Having unexpected error[' + str(number) + '], and the data type is not number.')
        return False


def get_math_nan_value():  # tested
    return math.nan


def get_decimal_value_position(number_value):
    position = 0
    try:
        while number_value < 1:
            position = position + 1
            number_value = number_value * 10
    except:
        acm.show_exception_message('Having unexpected error[' + str(number_value) + '], and the data type is not number.')
    return position


def get_power_value_position(number_value):
    position = 0
    try:
        while number_value > 1:
            position = position + 1
            number_value = number_value / 10
    except:
        acm.show_exception_message('Having unexpected error[' + str(number_value) + '], and the data type is not number.')
    return position
