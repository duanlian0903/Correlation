# tested
import api.operation.common.message as aocm


def initial_dict_with_empty_value(key_list, empty_value):  # tested
    result = {}
    try:
        for key in key_list:
            result[key] = empty_value
    except:
        aocm.show_exception_message('We generate an empty dictionary because of unexpected errors.')
    return result


def initial_dict_with_value_list(key_list, value_list):  # tested
    result = {}
    try:
        if len(key_list) == len(value_list):
            for i in range(len(key_list)):
                result[key_list[i]] = value_list[i]
        else:
            aocm.show_exception_message('We generate an empty dictionary because the length of key does not match the length of value.')
    except:
        aocm.show_exception_message('We generate an empty dictionary because of unexpected errors.')
    return result


def whether_all_empty_string_value_dict(dict_data):  # tested
    whether_empty_dict = True
    try:
        for key in dict_data:
            if dict_data[key] != '':
                whether_empty_dict = False
        return whether_empty_dict
    except:
        aocm.show_exception_message('We return false because of unexpected errors.')
        return False


def get_sorted_list(original_list, descending=False):
    return sorted(original_list, reverse=descending)


def get_indexed_dict_for_list(original_list):
    indexed_dict = {}
    for index in range(len(original_list)):
        indexed_dict[index] = original_list[index]
    return indexed_dict


def get_sorted_dict_by_value(original_dict, descending=False):
    return dict(sorted(original_dict.items(), key=lambda item: item[1], reverse=descending))


def get_sorted_dict_by_key(original_dict, descending=False):
    return dict(sorted(original_dict.items(), key=lambda item: item[0], reverse=descending))


def get_push_list(current_list, new_candidate, descending=True):
    position = 0
    index = 0
    while (index < len(current_list)-1) & (((current_list[index][1] > new_candidate[1]) & descending) | ((current_list[index][1] < new_candidate[1]) & (not descending))):
        index = index + 1
        position = index
    if (index == len(current_list)-1) & (((current_list[index][1] > new_candidate[1]) & descending) | ((current_list[index][1] < new_candidate[1]) & (not descending))):
        position = index + 1
    return current_list[:position]+[new_candidate]+current_list[position:]


def get_top_k_push_list(current_list, new_candidate, top_k, descending=True):
    # test get_top_k_push_list([(1, 4), (1, 3), (1, 2), (1, 1)], (2, 0.5), 4)
    top_k_push_list = current_list
    if ((current_list[-1][1] < new_candidate[1]) & descending) | ((current_list[-1][1] > new_candidate[1]) & (not descending)):
        if len(current_list) >= top_k:
            top_k_push_list = get_push_list(current_list, new_candidate, descending)[:top_k]
        else:
            top_k_push_list = get_push_list(current_list, new_candidate, descending)
    else:
        if len(current_list) < top_k:
            top_k_push_list.append(new_candidate)
    return top_k_push_list
