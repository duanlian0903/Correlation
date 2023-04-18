import api.data_load.transaction as adlt
import api.common.data_type.list_dict_set_tuple as acdtldst
import api.analytics.descriptive.correlation.measure as aadcm
import api.analytics.descriptive.correlation.contingency_table_correction as aadcctc
import api.analytics.descriptive.correlation.speed_up as aadcsu
import datetime as dt


def brute_force_search(transaction_dict, correlation_type, cc=0.5, whether_correct=True, target_p_value=0.05, delta=0.0001, whether_speed_up_screen=True):
    begin = dt.datetime.now()
    print(begin)
    item_frequency_dict = adlt.get_item_frequency_dict(transaction_dict)
    drug_list = []
    adr_list = []
    for item_key in item_frequency_dict:
        if item_key[0] == 'd':
            drug_list.append(item_key)
        if item_key[0] == 'a':
            adr_list.append(item_key)
    drug_list = sorted(drug_list)
    adr_list = sorted(adr_list)
    for drug in drug_list:
        for adr in adr_list:
            result = [drug, adr, aadcsu.get_pair_correlation_estimation(transaction_dict, item_frequency_dict, [drug, adr], correlation_type, cc, whether_correct, target_p_value, delta, whether_speed_up_screen)]
            #'''
            if result[2] > 100:
                print(result)
            #'''
    end = dt.datetime.now()
    print(end)
    print((end-begin).total_seconds())


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


tran_dict = adlt.get_transaction_dict('data/simulation/adr', 1000000)
small_tran_dict = {}
for key in tran_dict:
    if len(key) > 0:
        if (key[0] == 'a') | (key[0] == 'd'):
            if int(key[1:]) < 500:
                small_tran_dict[key] = tran_dict[key]
        else:
            small_tran_dict[key] = tran_dict[key]
brute_force_search(small_tran_dict, 'Relative Risk', whether_speed_up_screen=True)
brute_force_search(small_tran_dict, 'Relative Risk', whether_speed_up_screen=False)
'''
itemset = ['d1290', 'a614']
test1 = adlt.get_itemset_frequency(tran_dict, itemset)
test2 = adlt.get_itemset_ocp(tran_dict, itemset)
test3 = adlt.get_itemset_ecp(tran_dict, itemset)
test4 = adlt.get_contingency_table_dict(tran_dict, itemset[0], itemset[1])
test5 = aadcm.get_phi_coefficient_confidence_interval(adlt.get_contingency_table_dict(tran_dict, 'd1443', 'a2751'), 0.1)
test6 = aadcctc.get_corrected_contingency_table_dict(adlt.get_contingency_table_dict(tran_dict, 'd130', 'a2438'), 0.01)
check = 1
'''
