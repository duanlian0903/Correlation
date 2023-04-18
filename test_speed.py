import api.data_load.transaction as adlt
import api.common.data_type.list_dict_set_tuple as acdtldst
import api.analytics.descriptive.correlation.measure as aadcm
import api.analytics.descriptive.correlation.contingency_table_correction as aadcctc
import api.analytics.descriptive.correlation.speed_up as aadcsu
import datetime as dt


def brute_force_search(transaction_dict, correlation_type, correlation_threshold, cc=0.5, whether_correct=True, target_p_value=0.05, delta=0.0001, whether_speed_up_screen=True):
    begin = dt.datetime.now()
    print(begin)
    item_frequency_dict = adlt.get_item_frequency_dict(transaction_dict)
    drug_list = []
    adr_list = []
    result = []
    for item_key in item_frequency_dict:
        if item_key[0] == 'd':
            drug_list.append(item_key)
        if item_key[0] == 'a':
            adr_list.append(item_key)
    drug_list = sorted(drug_list)
    adr_list = sorted(adr_list)
    for drug in drug_list:
        for adr in adr_list:
            correlation_estimation = aadcsu.get_pair_correlation_estimation(transaction_dict, item_frequency_dict, [drug, adr], correlation_type, cc, whether_correct, target_p_value, delta, whether_speed_up_screen)
            if correlation_estimation > correlation_threshold:
                result.append([drug, adr, correlation_estimation])
                print(result[-1])
    end = dt.datetime.now()
    print(end)
    print('total time is', (end-begin).total_seconds())


def upperbound_screen_search(transaction_dict, correlation_type, cc=0.5, whether_correct=True, target_p_value=0.05, delta=0.0001):
    check = 1


def branch_individual_search(transaction_dict, correlation_type, cc=0.5, whether_correct=True, target_p_value=0.05, delta=0.0001):
    # we did the upperbound calculation for each pair in the queue
    item_frequency_dict = adlt.get_item_frequency_dict(transaction_dict)
    sorted_item_frequency_dict = acdtldst.get_sorted_dict_by_value(item_frequency_dict)
    check = 1


def branch_range_search(transaction_dict, correlation_type, cc=0.5, whether_correct=True, target_p_value=0.05, delta=0.0001):
    # we get a range for the valid occurrence of given item
    check = 1


def test_adr_simulation_data():
    tran_dict = adlt.get_transaction_dict('data/simulation/adr', 1000000)
    small_tran_dict = {}
    for key in tran_dict:
        if len(key) > 0:
            if (key[0] == 'a') | (key[0] == 'd'):
                if int(key[1:]) < 500:
                    small_tran_dict[key] = tran_dict[key]
            else:
                small_tran_dict[key] = tran_dict[key]
    correlation_type = 'Relative Risk'
    correlation_threshold = 100
    brute_force_search(small_tran_dict, correlation_type, correlation_threshold, whether_speed_up_screen=True)
    brute_force_search(small_tran_dict, correlation_type, correlation_threshold, whether_speed_up_screen=False)


test_adr_simulation_data()
