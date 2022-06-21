import api.operation.common.data_type.file_operation as aocdtfo


def transform_into_dict_data(transaction_file_folder):
    item_file = open(transaction_file_folder+'/item.txt', 'rt')
    transaction_file = open(transaction_file_folder+'/transaction.txt', 'rt')
    item_file_lines = item_file.readlines()
    transaction_file_lines = transaction_file.readlines()
    transaction_dict = {'n': len(transaction_file_lines)}
    for index in range(len(item_file_lines)):
        transaction_dict[index] = {'name': item_file_lines[index][:-1], 'tran_id_set': set()}
    for index in range(len(transaction_file_lines)):
        items_in_each_line = transaction_file_lines[index].split(',')
        for item in items_in_each_line:
            transaction_dict[int(item)]['tran_id_set'].add(index)
    aocdtfo.save_pickle_data(transaction_dict, transaction_file_folder+'/transaction_dict.pk', False)


def get_item_frequency_dict(transaction_dict):
    item_frequency_dict = {}
    for key in transaction_dict:
        if key == 'n':
            item_frequency_dict[key] = transaction_dict[key]
        else:
            item_frequency_dict[key] = len(transaction_dict[key]['tran_id_set'])
    return item_frequency_dict


def get_itemset_frequency(transaction_dict, itemset_tuple):
    overlapping_set = transaction_dict[itemset_tuple[0]]['tran_id_set']
    for item_id in itemset_tuple:
        overlapping_set = overlapping_set.intersection(transaction_dict[item_id]['tran_id_set'])
    return len(overlapping_set)


def get_itemset_ocp(transaction_dict, item_id_set):
    return get_itemset_frequency(transaction_dict, item_id_set)/transaction_dict['n']


def get_itemset_ecp(item_frequency_dict, item_id_set):
    itemset_ecp = 1
    for item_id in item_id_set:
        itemset_ecp = itemset_ecp * item_frequency_dict[item_id]/item_frequency_dict['n']
    return itemset_ecp
