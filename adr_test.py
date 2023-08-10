import api.analytics.descriptive.correlation.measure as aocadcm
import api.analytics.descriptive.correlation.contingency_table_correction as aocadcc
import api.analytics.evaluation as aocae
import api.common.data_type.file as aocdtfo
import pandas as pd
import math


def get_dataset_folder_name():
    return 'data/simulation/adr/'


def get_entire_transaction_file_data():
    tran_file = open(get_dataset_folder_name()+'s_transactions.txt')
    return tran_file.readlines()


def get_latent_true_correlation_df():
    return pd.read_csv(get_dataset_folder_name()+'groundTrueCorrelation.csv')


def get_latent_true_correlation_dict(attribute_name, independence_value, whether_log=False):
    latent_true_correlation_dict = {}
    for i in range(2000):
        drug_key = 'd'+str(i)
        for j in range(4000):
            adr_key = 'a'+str(j)
            if whether_log:
                latent_true_correlation_dict[drug_key+adr_key] = math.log(independence_value)
            else:
                latent_true_correlation_dict[drug_key+adr_key] = independence_value
    latent_true_correlation_df = get_latent_true_correlation_df()
    for index_id in latent_true_correlation_df.index:
        key_value = latent_true_correlation_df.loc[index_id, 'drugID']+latent_true_correlation_df.loc[index_id, 'adrID']
        if whether_log:
            latent_true_correlation_dict[key_value] = math.log(latent_true_correlation_df.loc[index_id, attribute_name])
        else:
            latent_true_correlation_dict[key_value] = latent_true_correlation_df.loc[index_id, attribute_name]
    return latent_true_correlation_dict


def get_relevance_score_list(correlation_df, attribute_name, latent_true_correlation_dict):
    correlation_df = correlation_df.sort_values(attribute_name, ascending=False)
    relevance_score_list = []
    for index_id in correlation_df.index:
        relevance_score_list.append(latent_true_correlation_dict[index_id])
    return relevance_score_list


def get_subset_transaction_file_data(entire_transaction_file_data, n):
    return entire_transaction_file_data[:n]


def get_transaction_dict(subset_transaction_file_data):
    transaction_dict = {'n': len(subset_transaction_file_data)}
    transaction_id = 0
    for line in subset_transaction_file_data:
        items = line[:-1].split(',')
        for item in items:
            if item in transaction_dict:
                transaction_dict[item].add(transaction_id)
            else:
                transaction_dict[item] = {transaction_id}
        transaction_id = transaction_id + 1
    return transaction_dict


def get_all_contingency_table_dict(transaction_dict):
    all_contingency_table_dict = {}
    for i in range(2000):
        drug_key = 'd'+str(i)
        drug_set = set()
        if drug_key in transaction_dict:
            drug_set = transaction_dict[drug_key]
        for j in range(4000):
            adr_key = 'a'+str(j)
            adr_set = set()
            if adr_key in transaction_dict:
                adr_set = transaction_dict[adr_key]
            union_set = drug_set.intersection(adr_set)
            n11 = len(union_set)
            n10 = len(drug_set)-n11
            n01 = len(adr_set)-n11
            all_contingency_table_dict[drug_key+adr_key] = {"n11": n11, "n10": n10, "n01": n01, "n00": transaction_dict['n']-n11-n10-n01}
    return all_contingency_table_dict


def get_alpha_list():
    alpha_list = []
    for i in range(1, 3):
        alpha_list = alpha_list + [10 ** (-i)]
    return alpha_list
    #return [5e-08, 5e-06, 0.0005, 0.005, 0.05, 0.5] #[1e-10, 1e-09, 1e-08, 1e-07, 1e-06, 1e-05, 0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]


def get_dataset_size_list():
    #return [1000000]
    return [10000, 100000]


def get_correlation_candidate_list():
    # AV, LV, OR, PR, RR (original, confidence interval, alpha)             CS, LR, BCPNN
    return ['CS', 'LR', 'BCPNN', 'OR_OR', 'PH_OR', 'OR_CI', 'PH_CI', 'OR_EC', 'PH_EC']
    # return ['CS', 'LR', 'BCPNN', 'AV_OR', 'LV_OR', 'OR_OR', 'PR_OR', 'RR_OR', 'PH_OR', 'AV_CI', 'LV_CI', 'OR_CI', 'PR_CI', 'RR_CI', 'PH_CI', 'AV_EC', 'LV_EC', 'OR_EC', 'PR_EC', 'RR_EC', 'PH_EC']


def get_basic_correlation_degree_dict(contingency_table_dict):
    n = contingency_table_dict['n11'] + contingency_table_dict['n10'] + contingency_table_dict['n01'] + contingency_table_dict['n00']
    tcp = contingency_table_dict['n11']/n
    ecp = (contingency_table_dict['n11'] + contingency_table_dict['n10'])/n*(contingency_table_dict['n11'] + contingency_table_dict['n01'])/n
    correlation_degree_dict = {#'CS': aocadcm.get_chi_square(tcp, ecp, n),
                        #'LR': aocadcm.get_likelihood_ratio(tcp, ecp, n),
                        'BCPNN': aocadcm.get_bcpnn(tcp, ecp, n),
                        'AV_OR': aocadcm.get_added_value(contingency_table_dict),
                        'LV_OR': aocadcm.get_probability_difference(tcp, ecp),
                        'OR_OR': aocadcm.get_odds_ratio(contingency_table_dict),
                        'PR_OR': aocadcm.get_probability_ratio(tcp, ecp),
                        'RR_OR': aocadcm.get_relative_risk(contingency_table_dict),
                        #'PH_OR': aocadcm.get_phi_coefficient(contingency_table_dict)
                        }
    return correlation_degree_dict


def get_cc_correlation_degree_dict(contingency_table_dict, cc=0.5):
    contingency_table_dict = aocadcc.get_cc_contingency_table_dict(contingency_table_dict, cc)
    basic_correlation_degree_dict = get_basic_correlation_degree_dict(contingency_table_dict)
    correlation_degree_dict = {}
    for key in basic_correlation_degree_dict:
        correlation_degree_dict[key+'_CC'] = basic_correlation_degree_dict[key]
    return correlation_degree_dict


def get_alpha_correlation_degree_dict(contingency_table_dict, alpha):
    n = contingency_table_dict['n11'] + contingency_table_dict['n10'] + contingency_table_dict['n01'] + contingency_table_dict['n00']
    tcp = contingency_table_dict['n11']/n
    ecp = (contingency_table_dict['n11'] + contingency_table_dict['n10'])/n*(contingency_table_dict['n11'] + contingency_table_dict['n01'])/n
    correlation_degree_dict = {}
    correlation_degree_dict['AV_CIL' + str(alpha)] = aocadcm.get_added_value_confidence_interval(contingency_table_dict, alpha)[0]
    correlation_degree_dict['LV_CIL' + str(alpha)] = aocadcm.get_probability_difference_confidence_interval(tcp, ecp, n, alpha)[0]
    correlation_degree_dict['OR_CIL' + str(alpha)] = aocadcm.get_odds_ratio_confidence_interval(contingency_table_dict, alpha)[0]
    correlation_degree_dict['PR_CIL' + str(alpha)] = aocadcm.get_probability_ratio_confidence_interval(tcp, ecp, n, alpha)[0]
    correlation_degree_dict['RR_CIL' + str(alpha)] = aocadcm.get_relative_risk_confidence_interval(contingency_table_dict, alpha)[0]
    #correlation_degree_dict['PH_CIL' + str(alpha)] = aocadcm.get_phi_coefficient_confidence_interval(contingency_table_dict, alpha)[0]
    #correlation_degree_dict['AV_CIC' + str(alpha)] = aocadcm.get_correlation_degree_confidence_interval_point_estimation(aocadcm.get_added_value_confidence_interval(contingency_table_dict, alpha), 0)
    #correlation_degree_dict['LV_CIC' + str(alpha)] = aocadcm.get_correlation_degree_confidence_interval_point_estimation(aocadcm.get_probability_difference_confidence_interval(tcp, ecp, n, alpha), 0)
    #correlation_degree_dict['OR_CIC' + str(alpha)] = aocadcm.get_correlation_degree_confidence_interval_point_estimation(aocadcm.get_odds_ratio_confidence_interval(contingency_table_dict, alpha), 1)
    #correlation_degree_dict['PR_CIC' + str(alpha)] = aocadcm.get_correlation_degree_confidence_interval_point_estimation(aocadcm.get_probability_ratio_confidence_interval(tcp, ecp, n, alpha), 1)
    #correlation_degree_dict['RR_CIC' + str(alpha)] = aocadcm.get_correlation_degree_confidence_interval_point_estimation(aocadcm.get_relative_risk_confidence_interval(contingency_table_dict, alpha), 1)
    #correlation_degree_dict['PH_CIC' + str(alpha)] = aocadcm.get_correlation_degree_confidence_interval_point_estimation(aocadcm.get_phi_coefficient_confidence_interval(contingency_table_dict, alpha), 0)
    '''
    correlation_degree_dict = {
        'AV_CIL' + str(alpha): aocadcm.get_added_value_confidence_interval(contingency_table_dict, alpha)[0],
        'LV_CIL' + str(alpha): aocadcm.get_probability_difference_confidence_interval(tcp, ecp, n, alpha)[0],
        'OR_CIL' + str(alpha): aocadcm.get_odds_ratio_confidence_interval(contingency_table_dict, alpha)[0],
        'PR_CIL' + str(alpha): aocadcm.get_probability_ratio_confidence_interval(tcp, ecp, n, alpha)[0],
        'RR_CIL' + str(alpha): aocadcm.get_relative_risk_confidence_interval(contingency_table_dict, alpha)[0],
        'PH_CIL' + str(alpha): aocadcm.get_phi_coefficient_confidence_interval(contingency_table_dict, alpha)[0],
        'AV_CIC' + str(alpha): aocadcm.get_correlation_degree_confidence_interval_point_estimation(aocadcm.get_added_value_confidence_interval(contingency_table_dict, alpha), 0),
        'LV_CIC' + str(alpha): aocadcm.get_correlation_degree_confidence_interval_point_estimation(aocadcm.get_probability_difference_confidence_interval(tcp, ecp, n, alpha), 0),
        'OR_CIC' + str(alpha): aocadcm.get_correlation_degree_confidence_interval_point_estimation(aocadcm.get_odds_ratio_confidence_interval(contingency_table_dict, alpha), 1),
        'PR_CIC' + str(alpha): aocadcm.get_correlation_degree_confidence_interval_point_estimation(aocadcm.get_probability_ratio_confidence_interval(tcp, ecp, n, alpha), 1),
        'RR_CIC' + str(alpha): aocadcm.get_correlation_degree_confidence_interval_point_estimation(aocadcm.get_relative_risk_confidence_interval(contingency_table_dict, alpha), 1),
        'PH_CIC' + str(alpha): aocadcm.get_correlation_degree_confidence_interval_point_estimation(aocadcm.get_phi_coefficient_confidence_interval(contingency_table_dict, alpha), 0)
    }
    #corrected_contingency_table_dict = aocadcc.get_lowerbound_corrected_contingency_table_dict(contingency_table_dict, alpha)
    #tcp = corrected_contingency_table_dict['n11']/n
    #ecp = (corrected_contingency_table_dict['n11'] + corrected_contingency_table_dict['n10'])/n*(corrected_contingency_table_dict['n11'] + corrected_contingency_table_dict['n01'])/n
    #correlation_degree_dict['AV_REL'+str(alpha)] = aocadcm.get_added_value(corrected_contingency_table_dict)
    #correlation_degree_dict['LV_REL'+str(alpha)] = aocadcm.get_probability_difference(tcp, ecp)
    #correlation_degree_dict['OR_REL'+str(alpha)] = aocadcm.get_odds_ratio(corrected_contingency_table_dict)
    #correlation_degree_dict['PR_REL'+str(alpha)] = aocadcm.get_probability_ratio(tcp, ecp)
    #correlation_degree_dict['RR_REL'+str(alpha)] = aocadcm.get_relative_risk(corrected_contingency_table_dict)
    #correlation_degree_dict['PH_REL'+str(alpha)] = aocadcm.get_phi_coefficient(corrected_contingency_table_dict)
    '''
    corrected_contingency_table_dict = aocadcc.get_corrected_contingency_table_dict(contingency_table_dict, alpha)
    tcp = corrected_contingency_table_dict['n11']/n
    ecp = (corrected_contingency_table_dict['n11'] + corrected_contingency_table_dict['n10'])/n*(corrected_contingency_table_dict['n11'] + corrected_contingency_table_dict['n01'])/n
    correlation_degree_dict['AV_REC'+str(alpha)] = aocadcm.get_added_value(corrected_contingency_table_dict)
    correlation_degree_dict['LV_REC'+str(alpha)] = aocadcm.get_probability_difference(tcp, ecp)
    correlation_degree_dict['OR_REC'+str(alpha)] = aocadcm.get_odds_ratio(corrected_contingency_table_dict)
    correlation_degree_dict['PR_REC'+str(alpha)] = aocadcm.get_probability_ratio(tcp, ecp)
    correlation_degree_dict['RR_REC'+str(alpha)] = aocadcm.get_relative_risk(corrected_contingency_table_dict)
    #correlation_degree_dict['PH_REC'+str(alpha)] = aocadcm.get_phi_coefficient(corrected_contingency_table_dict)
    return correlation_degree_dict


def calculate_dataset_correlation():
    dataset_size_list = get_dataset_size_list()
    alpha_list = get_alpha_list()
    for dataset_size in dataset_size_list:
        print('Start dataset size ' + str(dataset_size))
        entire_tran_file_data = get_entire_transaction_file_data()
        subset_tran_file_data = get_subset_transaction_file_data(entire_tran_file_data, dataset_size)
        tran_dict = get_transaction_dict(subset_tran_file_data)
        current_all_contingency_table_dict = get_all_contingency_table_dict(tran_dict)
        if not aocdtfo.check_file_existence(get_dataset_folder_name()+'cd.'+str(dataset_size)+'.pk'):
            matrix = []
            for pair in current_all_contingency_table_dict:
                row_dict = {'Name': pair}
                row_dict.update(get_basic_correlation_degree_dict(current_all_contingency_table_dict[pair]))
                matrix.append(row_dict)
            correlation_df = pd.DataFrame(matrix).set_index('Name')
            aocdtfo.save_pickle_data(correlation_df, get_dataset_folder_name()+'cd.'+str(dataset_size)+'.pk', False)
        for alpha in alpha_list:
            print('Start alpha ' + str(alpha))
            check = 1
            if not aocdtfo.check_file_existence(get_dataset_folder_name()+'cd.'+str(dataset_size)+'.'+str(alpha)+'.pk'):
                matrix = []
                for pair in current_all_contingency_table_dict:
                    row_dict = {'Name': pair}
                    row_dict.update(get_alpha_correlation_degree_dict(current_all_contingency_table_dict[pair], alpha))
                    matrix.append(row_dict)
                    #print(pair)
                correlation_df = pd.DataFrame(matrix).set_index('Name')
                aocdtfo.save_pickle_data(correlation_df, get_dataset_folder_name()+'cd.'+str(dataset_size)+'.'+str(alpha)+'.pk', False)


def evaluate_method():
    dataset_size_list = get_dataset_size_list()
    alpha_list = get_alpha_list()
    latent_true_attribute_para_list = [['Leverage', 0, False], ['PR', 1, True], ['AddedValue', 0, False], ['relative risk', 1, True], ['odds ratio', 1, True], ['phi', 0, False]]
    latent_true_attribute_para_list = [['odds ratio', 1, True], ['phi', 0, False]]
    for latent_true_attribute_para in latent_true_attribute_para_list:
        latent_true_correlation_dict = get_latent_true_correlation_dict(latent_true_attribute_para[0], latent_true_attribute_para[1], latent_true_attribute_para[2])
        for dataset_size in dataset_size_list:
            result_dict = {}
            correlation_df = aocdtfo.load_pickle_data(get_dataset_folder_name()+'cd.'+str(dataset_size)+'.pk')
            check = 1
            for column_name in correlation_df.columns:
                relevance_score_list = get_relevance_score_list(correlation_df, column_name, latent_true_correlation_dict)
                result_dict[column_name] = aocae.get_ranking_quality_score(relevance_score_list)
            for alpha in alpha_list:
                correlation_df = aocdtfo.load_pickle_data(get_dataset_folder_name()+'cd.'+str(dataset_size)+'.'+str(alpha)+'.pk')
                for column_name in correlation_df.columns:
                    relevance_score_list = get_relevance_score_list(correlation_df, column_name, latent_true_correlation_dict)
                    result_dict[column_name] = aocae.get_ranking_quality_score(relevance_score_list)
            aocdtfo.save_dict_as_json_file(result_dict, get_dataset_folder_name()+'result.'+str(latent_true_attribute_para[0])+'.'+str(dataset_size)+'.json')


def calculate_aki_correlation():
    raw_df = pd.read_csv('data/AKI/data.csv')
    alpha_list = get_alpha_list()
    matrix = []
    for i in raw_df.index:
        correlation_degree_dict = {}
        contingency_table_dict = {'n11': raw_df.loc[i, 'n11'], 'n10': raw_df.loc[i, 'n10'], 'n01': raw_df.loc[i, 'n01'], 'n00': raw_df.loc[i, 'n00']}
        correlation_degree_dict.update(get_basic_correlation_degree_dict(contingency_table_dict))
        for alpha in alpha_list:
            correlation_degree_dict.update(get_alpha_correlation_degree_dict(contingency_table_dict, alpha))
        matrix.append(correlation_degree_dict)
    correlation_df = pd.DataFrame(matrix)
    result_df = pd.concat([raw_df, correlation_df], axis=1)
    aocdtfo.save_pickle_data(result_df, 'data/AKI/result.pk', True)


def evaluate_aki():
    result_df = aocdtfo.load_pickle_data('data/AKI/result.pk')
    attribute_name_list = list(result_df.columns)
    result_dict = {}
    for attribute_name in attribute_name_list[8:]:
        result_df = result_df.sort_values(by=attribute_name, ascending=False)
        relevance_score_list = list(result_df[attribute_name_list[7]])
        result_dict[attribute_name] = aocae.get_ranking_quality_score(relevance_score_list)
    aocdtfo.save_dict_as_json_file(result_dict, 'data/AKI/rsq.json')


#calculate_aki_correlation()
#evaluate_aki()
#aocmt.embarrassing_parallel_process(calculate_dataset_correlation, [0, 1, 2, 3, 4], 1)
#evaluate_method()
calculate_dataset_correlation()
evaluate_method()
