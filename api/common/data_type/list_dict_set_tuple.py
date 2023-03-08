
def get_sorted_list(original_list, descending=False):
    return sorted(original_list, reverse=descending)


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
