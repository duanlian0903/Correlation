import api.operation.common.analytics.descriptive.correlation.data as aocadcd
import api.operation.common.analytics.descriptive.correlation.correction as aocadcc
import api.operation.common.analytics.descriptive.correlation.measure as aocadcm
import api.operation.common.data_type.list_dict_set_tuple as aocdtldst


def pair_correlation_function(n11, item_frequency_dict, pair_tuple, correlation_type, cc=0.5, whether_correct=True, target_p_value=0.05, delta=0.0001):
    contingency_table_dict = {'n11': n11, 'n10': item_frequency_dict[pair_tuple[0]]-n11, 'n01': item_frequency_dict[pair_tuple[1]]-n11, 'n00': item_frequency_dict['n'] - item_frequency_dict[pair_tuple[0]] - item_frequency_dict[pair_tuple[1]] + n11}
    if whether_correct:
        contingency_table_dict = aocadcc.get_corrected_contingency_table_dict(contingency_table_dict, target_p_value, delta)
    return aocadcm.get_pair_correlation(contingency_table_dict, correlation_type, cc)


def get_pair_correlation_estimation(transaction_dict, item_frequency_dict, pair_tuple, correlation_type, cc=0.5, whether_correct=True, target_p_value=0.05, delta=0.0001):
    n11 = aocadcd.get_itemset_frequency(transaction_dict, pair_tuple)
    return pair_correlation_function(n11, item_frequency_dict, pair_tuple, correlation_type, cc, whether_correct, target_p_value, delta)


def get_pair_correlation_upperbound(item_frequency_dict, pair_tuple, correlation_type, cc=0.5, whether_correct=True, target_p_value=0.05, delta=0.0001):
    n11 = min(item_frequency_dict[pair_tuple[0]], item_frequency_dict[pair_tuple[1]])
    return pair_correlation_function(n11, item_frequency_dict, pair_tuple, correlation_type, cc, whether_correct, target_p_value, delta)


def get_top_k_pairs_by_token_ring(transaction_dict, top_k, correlation_type, cc=0.5, whether_correct=False, target_p_value=0.05, delta=0.0001):
    item_frequency_dict = aocadcd.get_item_frequency_dict(transaction_dict)
    item_id_list = list(aocdtldst.get_sorted_dict_by_value(item_frequency_dict).keys())[:-1]
    top_k_list = []
    token_ring_dict = {}
    for i in range(len(item_id_list)-1):
        token_ring_dict[i] = i+1
    while len(token_ring_dict) > 0:
        current_key_list = list(token_ring_dict.keys())
        for key in current_key_list:
            pair_tuple = (item_id_list[key], item_id_list[token_ring_dict[key]])
            if len(top_k_list) > 0:
                pair_correlation_upperbound = get_pair_correlation_upperbound(item_frequency_dict, pair_tuple, correlation_type, cc, whether_correct, target_p_value, delta)
                if pair_correlation_upperbound > top_k_list[-1][1]:
                    # we start to calculate real correlation
                    pair_correlation_estimation = get_pair_correlation_estimation(transaction_dict, item_frequency_dict, pair_tuple, correlation_type, cc, whether_correct, target_p_value, delta)
                    if pair_correlation_estimation > top_k_list[-1][1]:
                        top_k_list = aocdtldst.get_top_k_push_list(top_k_list, (pair_tuple, pair_correlation_estimation), top_k)
                    if token_ring_dict[key] < len(item_id_list) - 1:
                        token_ring_dict[key] = token_ring_dict[key] + 1
                    else:
                        del token_ring_dict[key]
                else:
                    del token_ring_dict[key]
            else:
                # when the top k list is still empty
                top_k_list.append((pair_tuple, get_pair_correlation_estimation(transaction_dict, item_frequency_dict, pair_tuple, correlation_type, cc, whether_correct, target_p_value, delta)))
                token_ring_dict[key] = token_ring_dict[key] + 1
    return top_k_list
