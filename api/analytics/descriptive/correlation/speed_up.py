import api.data_load.transaction as aocadcd
import api.analytics.descriptive.correlation.contingency_table_correction as aocadcc
import api.analytics.descriptive.correlation.measure as aocadcm
import api.common.data_type.list_dict_set_tuple as aocdtldst


def pair_correlation_function(n11, item_frequency_dict, pair_tuple, correlation_type, cc=0.5, whether_correct=True, target_p_value=0.05, delta=0.0001, whether_speed_up_screen=True):
    contingency_table_dict = {'n11': n11, 'n10': item_frequency_dict[pair_tuple[0]]-n11, 'n01': item_frequency_dict[pair_tuple[1]]-n11, 'n00': item_frequency_dict['total_number_of_record'] - item_frequency_dict[pair_tuple[0]] - item_frequency_dict[pair_tuple[1]] + n11}
    if whether_correct:
        contingency_table_dict = aocadcc.get_corrected_contingency_table_dict(contingency_table_dict, target_p_value, delta, whether_speed_up_screen)
    return aocadcm.get_pair_correlation(contingency_table_dict, correlation_type, cc)


def get_pair_correlation_estimation(transaction_dict, item_frequency_dict, pair_tuple, correlation_type, cc=0.5, whether_correct=True, target_p_value=0.05, delta=0.0001, whether_speed_up_screen=True):
    n11 = aocadcd.get_itemset_frequency(transaction_dict, pair_tuple)
    return pair_correlation_function(n11, item_frequency_dict, pair_tuple, correlation_type, cc, whether_correct, target_p_value, delta, whether_speed_up_screen)


def get_relaxed_correlation_upperbound(item_frequency_dict, pair_tuple, correlation_type, cc=0.5):
    return get_pair_correlation_upperbound_with_raw_value(item_frequency_dict, pair_tuple, correlation_type, cc, whether_correct=False)


def get_corrected_n11_upperbound(item_frequency_dict, pair_tuple, target_p_value=0.05, delta=0.0001):
    # get related corrected n11 for a branch
    observed_prob = min(item_frequency_dict[pair_tuple[0]], item_frequency_dict[pair_tuple[1]])/item_frequency_dict['total_number_of_record']
    return aocadcc.bound_dict_for_likelihood_ratio_test_with_binomial_distribution(observed_prob, item_frequency_dict['total_number_of_record'], target_p_value, delta)['lowerbound']*item_frequency_dict['total_number_of_record']


def get_pair_correlation_upperbound_with_corrected_n11_upperbound(corrected_n11_upperbound, item_frequency_dict, pair_tuple, correlation_type, cc=0.5):
    return pair_correlation_function(corrected_n11_upperbound, item_frequency_dict, pair_tuple, correlation_type, cc=cc, whether_correct=False)


def get_pair_correlation_upperbound_with_raw_value(item_frequency_dict, pair_tuple, correlation_type, cc=0.5, whether_correct=True, target_p_value=0.05, delta=0.0001, whether_speed_up_screen=True):
    # get upperbound for a specific pair
    n11 = min(item_frequency_dict[pair_tuple[0]], item_frequency_dict[pair_tuple[1]])
    return pair_correlation_function(n11, item_frequency_dict, pair_tuple, correlation_type, cc, whether_correct, target_p_value, delta, whether_speed_up_screen)


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
                pair_correlation_upperbound = get_pair_correlation_upperbound_with_raw_value(item_frequency_dict, pair_tuple, correlation_type, cc, whether_correct, target_p_value, delta)
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
