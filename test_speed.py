import api.data_load.transaction as adlt
import api.common.data_type.list_dict_set_tuple as acdtldst
import api.analytics.descriptive.correlation.measure as aadcm
import api.analytics.descriptive.correlation.speed_up as aadcsu
import datetime as dt


def brute_force_search(transaction_dict, correlation_type, correlation_threshold, cc=0.5, whether_correct=True, target_p_value=0.05, delta=0.0001, whether_speed_up_screen=True):
    begin = dt.datetime.now()
    print(begin, 'start brute force search with speed up screen', whether_speed_up_screen)
    item_frequency_dict = adlt.get_item_frequency_dict(transaction_dict)
    drug_list = []
    adr_list = []
    result = []
    for item_key in item_frequency_dict:
        if len(item_key) > 0:
            if item_key[0] == 'd':
                drug_list.append(item_key)
            if item_key[0] == 'a':
                adr_list.append(item_key)
    drug_list = sorted(drug_list)
    adr_list = sorted(adr_list)
    no_correlation_value = aadcm.get_pair_correlation({'n11': 25, 'n01': 25, 'n10': 25, 'n00': 25}, correlation_type)
    speed_up_count = 0
    non_speed_up_count = 0
    for drug in drug_list:
        for adr in adr_list:
            correlation_estimation = aadcsu.get_pair_correlation_estimation_with_given_transaction_dict(transaction_dict, item_frequency_dict, [drug, adr], correlation_type, cc, whether_correct, target_p_value, delta, whether_speed_up_screen)
            if (correlation_estimation > no_correlation_value + 0.000001) | (correlation_estimation < no_correlation_value - 0.000001):
                non_speed_up_count = non_speed_up_count + 1
            else:
                speed_up_count = speed_up_count + 1
            if correlation_estimation > correlation_threshold:
                result.append([drug, adr, correlation_estimation])
                #print(result[-1])
    end = dt.datetime.now()
    print('total time is', (end-begin).total_seconds(), '. speed up count:', speed_up_count, '. non speed up count:', non_speed_up_count, '. result len:', len(result))


def upperbound_screen_search(transaction_dict, correlation_type, correlation_threshold, whether_relaxed_upperbound=True, cc=0.5, whether_correct=True, target_p_value=0.05, delta=0.0001, whether_speed_up_screen=True, whether_get_candidate_list=True):
    begin = dt.datetime.now()
    print(begin, 'start upperbound search with relaxed upperbound', whether_relaxed_upperbound)
    item_frequency_dict = adlt.get_item_frequency_dict(transaction_dict)
    drug_list = []
    adr_list = []
    result = []
    for item_key in item_frequency_dict:
        if len(item_key) > 0:
            if item_key[0] == 'd':
                drug_list.append(item_key)
            if item_key[0] == 'a':
                adr_list.append(item_key)
    drug_list = sorted(drug_list)
    adr_list = sorted(adr_list)
    no_correlation_value = aadcm.get_pair_correlation({'n11': 25, 'n01': 25, 'n10': 25, 'n00': 25}, correlation_type)
    speed_up_count = 0
    non_speed_up_count = 0
    count_upperbound = 0
    count_estimation = 0
    for drug in drug_list:
        for adr in adr_list:
            count_upperbound = count_upperbound + 1
            correlation_upperbound = aadcsu.get_pair_correlation_upperbound_with_given_pair_tuple(item_frequency_dict, [drug, adr], correlation_type, cc, not whether_relaxed_upperbound, target_p_value, delta, whether_speed_up_screen)
            if correlation_upperbound > correlation_threshold:
                count_estimation = count_estimation + 1
                #'''
                if whether_get_candidate_list:
                    result.append([drug, adr])
                '''
                correlation_estimation = aadcsu.get_pair_correlation_estimation_with_given_transaction_dict(transaction_dict, item_frequency_dict, [drug, adr], correlation_type, cc, whether_correct, target_p_value, delta, whether_speed_up_screen)
                if (correlation_estimation > no_correlation_value + 0.000001) | (correlation_estimation < no_correlation_value - 0.000001):
                    non_speed_up_count = non_speed_up_count + 1
                else:
                    speed_up_count = speed_up_count + 1
                if correlation_estimation > correlation_threshold:
                    result.append([drug, adr, correlation_estimation])
                    #print(result[-1])
                #'''
    end = dt.datetime.now()
    print('total time is', (end-begin).total_seconds(), '. upperbound count:', count_upperbound, '. estimation count:', count_estimation, '. speed up count:', speed_up_count, '. non speed up count:', non_speed_up_count, '. result len:', len(result))
    return result


def branch_individual_search(transaction_dict, correlation_type, correlation_threshold, whether_relaxed_upperbound=True, cc=0.5, whether_correct=True, target_p_value=0.05, delta=0.0001, whether_speed_up_screen=True, whether_get_candidate_list=True):
    begin = dt.datetime.now()
    print(begin, 'start branch individual search with relaxed upperbound', whether_relaxed_upperbound)
    item_frequency_dict = adlt.get_item_frequency_dict(transaction_dict)
    sorted_item_frequency_dict = acdtldst.get_sorted_dict_by_value(item_frequency_dict)
    item_list = list(sorted_item_frequency_dict.keys())
    if '' in item_list:
        item_list.remove('')
    if 'total_number_of_record' in item_list:
        item_list.remove('total_number_of_record')
    no_correlation_value = aadcm.get_pair_correlation({'n11': 25, 'n01': 25, 'n10': 25, 'n00': 25}, correlation_type)
    speed_up_count = 0
    non_speed_up_count = 0
    count_upperbound = 0
    count_estimation = 0
    result = []
    for i in range(len(item_list)-1):
        first_item = item_list[i]
        j = i + 1
        while j < len(item_list):
            second_item = item_list[j]
            if first_item[0] != second_item[0]:
                if first_item[0] == 'd':
                    pair_tuple = [first_item, second_item]
                else:
                    pair_tuple = [second_item, first_item]
                count_upperbound = count_upperbound + 1
                upperbound = aadcsu.get_pair_correlation_upperbound_with_given_pair_tuple(item_frequency_dict, pair_tuple, correlation_type, cc, not whether_relaxed_upperbound, target_p_value, delta, whether_speed_up_screen)
                if upperbound < correlation_threshold:
                    j = len(item_list)
                else:
                    count_estimation = count_estimation + 1
                    #'''
                    if whether_get_candidate_list:
                        result.append(pair_tuple)
                    '''
                    correlation_estimation = aadcsu.get_pair_correlation_estimation_with_given_transaction_dict(transaction_dict, item_frequency_dict, pair_tuple, correlation_type, cc, whether_correct, target_p_value, delta, whether_speed_up_screen)
                    if (correlation_estimation > no_correlation_value + 0.000001) | (correlation_estimation < no_correlation_value - 0.000001):
                        non_speed_up_count = non_speed_up_count + 1
                    else:
                        speed_up_count = speed_up_count + 1
                    if correlation_estimation > correlation_threshold:
                        result.append([pair_tuple[0], pair_tuple[1], correlation_estimation])
                        #print(result[-1])
                    #'''
            j = j + 1
    end = dt.datetime.now()
    print('total time is', (end-begin).total_seconds(), '. upperbound count:', count_upperbound, '. estimation count:', count_estimation, '. speed up count:', speed_up_count, '. non speed up count:', non_speed_up_count, '. result len:', len(result))
    return result


def branch_range_search(transaction_dict, correlation_type, correlation_threshold, whether_general_half_search=True, whether_relaxed_upperbound=True, cc=0.5, whether_correct=True, target_p_value=0.05, delta=0.0001, whether_speed_up_screen=True, whether_get_candidate_list=True):
    begin = dt.datetime.now()
    print(begin, 'start branch range search with relaxed upperbound', whether_relaxed_upperbound, 'and general half search', whether_general_half_search)
    item_frequency_dict = adlt.get_item_frequency_dict(transaction_dict)
    sorted_item_frequency_dict = acdtldst.get_sorted_dict_by_value(item_frequency_dict)
    item_list = list(sorted_item_frequency_dict.keys())
    if '' in item_list:
        item_list.remove('')
    if 'total_number_of_record' in item_list:
        item_list.remove('total_number_of_record')
    no_correlation_value = aadcm.get_pair_correlation({'n11': 25, 'n01': 25, 'n10': 25, 'n00': 25}, correlation_type)
    speed_up_count = 0
    non_speed_up_count = 0
    count_upperbound = 0
    count_estimation = 0
    result = []
    for i in range(len(item_list)-1):
        first_item = item_list[i]
        count_upperbound = count_upperbound + 1
        if (correlation_type in ['Relative Risk', 'Odds Ratio']) & whether_relaxed_upperbound:
            occurrence_threshold = item_frequency_dict['total_number_of_record'] + 1
        else:
            if first_item[0] == 'd':
                if whether_general_half_search:
                    occurrence_threshold = aadcsu.get_outcome_range_by_half_search(item_frequency_dict[first_item], item_frequency_dict['total_number_of_record'], correlation_type, correlation_threshold * 0.99, whether_relaxed_upperbound, cc, whether_correct, target_p_value, delta, whether_speed_up_screen)
                else:
                    occurrence_threshold = aadcsu.get_outcome_range_by_formula(item_frequency_dict[first_item], item_frequency_dict['total_number_of_record'], correlation_type, correlation_threshold, whether_relaxed_upperbound, cc, whether_correct, target_p_value, delta, whether_speed_up_screen)
            else:
                if whether_general_half_search:
                    occurrence_threshold = aadcsu.get_intervention_range_by_half_search(item_frequency_dict[first_item], item_frequency_dict['total_number_of_record'], correlation_type, correlation_threshold * 0.99, whether_relaxed_upperbound, cc, whether_correct, target_p_value, delta, whether_speed_up_screen)
                else:
                    occurrence_threshold = aadcsu.get_intervention_range_by_formula(item_frequency_dict[first_item], item_frequency_dict['total_number_of_record'], correlation_type, correlation_threshold, whether_relaxed_upperbound, cc, whether_correct, target_p_value, delta, whether_speed_up_screen)
        j = i + 1
        while j < len(item_list):
            second_item = item_list[j]
            if first_item[0] != second_item[0]:
                if item_frequency_dict[second_item] < occurrence_threshold:
                    if first_item[0] == 'd':
                        pair_tuple = [first_item, second_item]
                    else:
                        pair_tuple = [second_item, first_item]
                    count_estimation = count_estimation + 1
                    #'''
                    if whether_get_candidate_list:
                        result.append(pair_tuple)
                    '''
                    correlation_estimation = aadcsu.get_pair_correlation_estimation_with_given_transaction_dict(transaction_dict, item_frequency_dict, pair_tuple, correlation_type, cc, whether_correct, target_p_value, delta, whether_speed_up_screen)
                    if (correlation_estimation > no_correlation_value + 0.000001) | (correlation_estimation < no_correlation_value - 0.000001):
                        non_speed_up_count = non_speed_up_count + 1
                    else:
                        speed_up_count = speed_up_count + 1
                    if correlation_estimation > correlation_threshold:
                        result.append([pair_tuple[0], pair_tuple[1], correlation_estimation])
                        #print(result[-1])
                    #'''
            j = j + 1
    end = dt.datetime.now()
    print('total time is', (end-begin).total_seconds(), '. upperbound count:', count_upperbound, '. estimation count:', count_estimation, '. speed up count:', speed_up_count, '. non speed up count:', non_speed_up_count, '. result len:', len(result))
    return result


def get_second_step_result(first_step_result, transaction_dict, correlation_type, correlation_threshold, cc=0.5, whether_correct=True, target_p_value=0.05, delta=0.0001, whether_speed_up_screen=True):
    item_frequency_dict = adlt.get_item_frequency_dict(transaction_dict)
    no_correlation_value = aadcm.get_pair_correlation({'n11': 25, 'n01': 25, 'n10': 25, 'n00': 25}, correlation_type)
    speed_up_count = 0
    non_speed_up_count = 0
    begin = dt.datetime.now()
    result = []
    for each_pair in first_step_result:
        correlation_estimation = aadcsu.get_pair_correlation_estimation_with_given_transaction_dict(transaction_dict, item_frequency_dict, each_pair, correlation_type, cc, whether_correct, target_p_value, delta, whether_speed_up_screen)
        if (correlation_estimation > no_correlation_value + 0.000001) | (correlation_estimation < no_correlation_value - 0.000001):
            non_speed_up_count = non_speed_up_count + 1
        else:
            speed_up_count = speed_up_count + 1
        if correlation_estimation > correlation_threshold:
            result.append([each_pair[0], each_pair[1], correlation_estimation])
    end = dt.datetime.now()
    print('total time is', (end-begin).total_seconds(), '. speed up count:', speed_up_count, '. non speed up count:', non_speed_up_count, '. result len:', len(result))
    return result


def get_all_actual_ecc(cc=0.5, whether_correct=True, target_p_value=0.05, delta=0.0001, whether_speed_up_screen=True):
    transaction_dict = adlt.get_transaction_dict('data/real/NewFAERS')
    item_frequency_dict = adlt.get_item_frequency_dict(transaction_dict)
    drug_list = []
    adr_list = []
    for item_key in item_frequency_dict:
        if len(item_key) > 0:
            if item_key[0] == 'd':
                drug_list.append(item_key)
            if item_key[0] == 'a':
                adr_list.append(item_key)
    drug_list = sorted(drug_list)
    adr_list = sorted(adr_list)
    for correlation_type in ['Added Value', 'Odds Ratio', 'Probability Difference', 'Probability Ratio', 'Relative Risk']:
        no_correlation_value = aadcm.get_pair_correlation({'n11': 25, 'n01': 25, 'n10': 25, 'n00': 25}, correlation_type)
        speed_up_count = 0
        non_speed_up_count = 0
        file = open('data/'+correlation_type+str(target_p_value)+'.csv', 'wt')
        file.write('drug,adr,'+correlation_type+'\n')
        for drug in drug_list:
            for adr in adr_list:
                correlation_estimation = aadcsu.get_pair_correlation_estimation_with_given_transaction_dict(transaction_dict, item_frequency_dict, [drug, adr], correlation_type, cc, whether_correct, target_p_value, delta, whether_speed_up_screen)
                if (correlation_estimation > no_correlation_value + 0.000001) | (correlation_estimation < no_correlation_value - 0.000001):
                    non_speed_up_count = non_speed_up_count + 1
                else:
                    speed_up_count = speed_up_count + 1
                file.write(drug+', '+adr+', '+str(correlation_estimation)+'\n')
        file.close()
        print(dt.datetime.now(), correlation_type, speed_up_count, non_speed_up_count)


def split_test():
    tran_dict = adlt.get_transaction_dict('data/real/NewFAERS')
    test_tran_dict = {}
    for key in tran_dict:
        if len(key) > 0:
            if (key[0] == 'a') | (key[0] == 'd'):
                if int(key[1:]) < 50:
                    test_tran_dict[key] = tran_dict[key]
            else:
                test_tran_dict[key] = tran_dict[key]
    test_tran_dict = tran_dict
    # when alpha=0.05, we have 1% ECC
    # added value: 1000: 0.18, 100: 0.4, 20: 0.6
    test_setting_list = [['Relative Risk', 10000], ['Probability Difference', 0.001], ['Probability Ratio', 10000], ['Added Value', 0.3], ['Odds Ratio', 10000]]
    test_setting_list = [['Added Value', 0.7], ['Added Value', 0.4], ['Added Value', 0.3], ['Added Value', 0.2], ['Added Value', 0.1], ['Added Value', 0.08], ['Added Value', 0.05],
                         ['Odds Ratio', 50000], ['Odds Ratio', 10000], ['Odds Ratio', 5000], ['Odds Ratio', 2000], ['Odds Ratio', 1000], ['Odds Ratio', 500], ['Odds Ratio', 200],
                         ['Probability Difference', 0.003], ['Probability Difference', 0.001], ['Probability Difference', 0.0006], ['Probability Difference', 0.0003], ['Probability Difference', 0.0002], ['Probability Difference', 0.0001], ['Probability Difference', 0.00005],
                         ['Probability Ratio', 50000], ['Probability Ratio', 10000], ['Probability Ratio', 5000], ['Probability Ratio', 2000], ['Probability Ratio', 1000], ['Probability Ratio', 500], ['Probability Ratio', 200],
                         ['Relative Risk', 50000], ['Relative Risk', 10000], ['Relative Risk', 5000], ['Relative Risk', 2000], ['Relative Risk', 1000], ['Relative Risk', 500], ['Relative Risk', 200]
                         ]
    for para_list in test_setting_list:
        print('\nwhen', para_list)
        correlation_type = para_list[0]
        correlation_threshold = para_list[1]
        first_result = branch_range_search(test_tran_dict, correlation_type, correlation_threshold, whether_general_half_search=False, whether_relaxed_upperbound=False, whether_get_candidate_list=False)
        #result = get_second_step_result(first_result, test_tran_dict, correlation_type, correlation_threshold)
        #print(result)


def test_adr_simulation_data():
    tran_dict = adlt.get_transaction_dict('data/simulation/adr', 1000000)
    test_tran_dict = {}
    for key in tran_dict:
        if len(key) > 0:
            if (key[0] == 'a') | (key[0] == 'd'):
                if int(key[1:]) < 50:
                    test_tran_dict[key] = tran_dict[key]
            else:
                test_tran_dict[key] = tran_dict[key]
    test_tran_dict = tran_dict
    for para_list in [['Relative Risk', 10000], ['Probability Difference', 0.001], ['Probability Ratio', 10000], ['Added Value', 0.3], ['Odds Ratio', 10000]]:
        print('when', para_list)
        correlation_type = para_list[0]
        correlation_threshold = para_list[1]
        branch_range_search(test_tran_dict, correlation_type, correlation_threshold, whether_general_half_search=False, whether_relaxed_upperbound=True)
        print()
        branch_range_search(test_tran_dict, correlation_type, correlation_threshold, whether_general_half_search=False, whether_relaxed_upperbound=False)
        print()
        branch_range_search(test_tran_dict, correlation_type, correlation_threshold, whether_general_half_search=True, whether_relaxed_upperbound=True)
        print()
        branch_range_search(test_tran_dict, correlation_type, correlation_threshold, whether_general_half_search=True, whether_relaxed_upperbound=False)
        print()
        brute_force_search(test_tran_dict, correlation_type, correlation_threshold, whether_speed_up_screen=True)
        print()
        brute_force_search(test_tran_dict, correlation_type, correlation_threshold, whether_speed_up_screen=False)
        print()
        upperbound_screen_search(test_tran_dict, correlation_type, correlation_threshold, whether_relaxed_upperbound=True)
        print()
        upperbound_screen_search(test_tran_dict, correlation_type, correlation_threshold, whether_relaxed_upperbound=False)
        print()
        branch_individual_search(test_tran_dict, correlation_type, correlation_threshold, whether_relaxed_upperbound=True)
        print()
        branch_individual_search(test_tran_dict, correlation_type, correlation_threshold, whether_relaxed_upperbound=False)
        print()



#test_adr_simulation_data()
split_test()
#get_all_actual_ecc()

