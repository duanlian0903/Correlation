import math


def get_total_number_of_record_attribute():
    return 'total_number_of_record'


def get_transaction_dict(transaction_file_folder, counted_number_of_record=math.inf):
    transaction_file = open(transaction_file_folder+'/transaction.txt', 'rt')
    transaction_file_lines = transaction_file.readlines()
    if len(transaction_file_lines) > counted_number_of_record:
        transaction_file_lines = transaction_file_lines[:counted_number_of_record]
    transaction_dict = {get_total_number_of_record_attribute(): len(transaction_file_lines)}
    for index in range(len(transaction_file_lines)):
        items_in_each_line = transaction_file_lines[index][:-1].split(',')
        for item in items_in_each_line:
            if item in transaction_dict:
                transaction_dict[item].add(index)
            else:
                transaction_dict[item] = set([index])
    return transaction_dict


def get_item_frequency_dict(transaction_dict):
    item_frequency_dict = {}
    for key in transaction_dict:
        if key == get_total_number_of_record_attribute():
            item_frequency_dict[key] = transaction_dict[key]
        else:
            item_frequency_dict[key] = len(transaction_dict[key])
    return item_frequency_dict


def get_itemset_frequency(transaction_dict, itemset_tuple):
    overlapping_set = transaction_dict[itemset_tuple[0]]
    for item_id in itemset_tuple:
        overlapping_set = overlapping_set.intersection(transaction_dict[item_id])
    return len(overlapping_set)


def get_itemset_ocp(transaction_dict, itemset_tuple):
    return get_itemset_frequency(transaction_dict, itemset_tuple) / transaction_dict[get_total_number_of_record_attribute()]


def get_itemset_ecp(transaction_dict, itemset_tuple):
    itemset_ecp = 1
    for item_id in itemset_tuple:
        itemset_ecp = itemset_ecp * len(transaction_dict[item_id])/transaction_dict[get_total_number_of_record_attribute()]
    return itemset_ecp


def get_contingency_table_dict(transaction_dict, first_item, second_item):
    n11 = get_itemset_frequency(transaction_dict, [first_item, second_item])
    n10 = len(transaction_dict[first_item]) - n11
    n01 = len(transaction_dict[second_item]) - n11
    n00 = transaction_dict[get_total_number_of_record_attribute()] - n11 - n10 - n01
    return {'n11': n11, 'n10': n10, 'n01': n01, 'n00': n00}
