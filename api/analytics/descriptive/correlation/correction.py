import api.analytics.descriptive.distribution.conversion_between_p_value_and_statistic_score as aaddcbpvass
import api.analytics.descriptive.distribution.statistic_score as aaddss
import api.analytics.prescriptive.half_interval_search as aaphis
import api.common.data_type.number_text_boolean as acdtntb


def likelihood_ratio_p_value_with_binomial_distribution(observed_prob, null_prob, n):
    likelihood_ratio_score = aaddss.likelihood_ratio_score_for_binomial_distribution(observed_prob, null_prob, n)
    return aaddcbpvass.get_p_value_from_chi_square(likelihood_ratio_score, degree_of_freedom=1)


def likelihood_ratio_p_value_with_binomial_distribution_monotonic_function(null_prob, para_dict):
    return likelihood_ratio_p_value_with_binomial_distribution(para_dict['observed_prob'], null_prob, para_dict['n'])


def bound_dict_for_likelihood_ratio_test_with_binomial_distribution(observed_prob, n, target_p_value, delta=0.0001):
    decimal_value_position = acdtntb.get_decimal_value_position(target_p_value)
    delta = delta / (10**decimal_value_position)
    return {'upperbound': aaphis.get_target_input_value(target_p_value, likelihood_ratio_p_value_with_binomial_distribution_monotonic_function, 1, observed_prob, {'observed_prob': observed_prob, 'n': n}, delta),
            'lowerbound': aaphis.get_target_input_value(target_p_value, likelihood_ratio_p_value_with_binomial_distribution_monotonic_function, observed_prob, 0, {'observed_prob': observed_prob, 'n': n}, delta)}


def corrected_observed_prob_for_likelihood_ratio_test_with_binomial_distribution(observed_prob, null_prob, n, target_p_value, delta=0.0001):
    corrected_observed_prob = null_prob
    if likelihood_ratio_p_value_with_binomial_distribution(observed_prob, null_prob, n) < target_p_value:
        bound_dict = bound_dict_for_likelihood_ratio_test_with_binomial_distribution(observed_prob, n, target_p_value, delta)
        if null_prob < bound_dict['lowerbound']:
            corrected_observed_prob = bound_dict['lowerbound']
        else:
            corrected_observed_prob = bound_dict['upperbound']
    return corrected_observed_prob


def get_corrected_contingency_table_dict(contingency_table_dict, target_p_value, delta=0.0001):
    n = contingency_table_dict['n11'] + contingency_table_dict['n10'] + contingency_table_dict['n01'] + contingency_table_dict['n00']
    ocp = contingency_table_dict['n11'] / n
    ecp = (contingency_table_dict['n11'] + contingency_table_dict['n10']) / n * (contingency_table_dict['n11'] + contingency_table_dict['n01']) / n
    corrected_ocp = corrected_observed_prob_for_likelihood_ratio_test_with_binomial_distribution(ocp, ecp, n, target_p_value, delta)
    return {'n11': corrected_ocp*n, 'n10': contingency_table_dict['n11'] + contingency_table_dict['n10'] - corrected_ocp * n,
            'n01': contingency_table_dict['n11'] + contingency_table_dict['n01'] - corrected_ocp * n, 'n00': contingency_table_dict['n00'] - contingency_table_dict['n11'] + corrected_ocp * n}


def get_lowerbound_corrected_contingency_table_dict(contingency_table_dict, target_p_value, delta=0.0001):
    n = contingency_table_dict['n11'] + contingency_table_dict['n10'] + contingency_table_dict['n01'] + contingency_table_dict['n00']
    ocp = contingency_table_dict['n11'] / n
    corrected_ocp = ocp
    if (ocp != 0) & (ocp != 1):
        bound_dict = bound_dict_for_likelihood_ratio_test_with_binomial_distribution(ocp, n, target_p_value, delta)
        corrected_ocp = bound_dict['lowerbound']
    return {'n11': corrected_ocp*n, 'n10': contingency_table_dict['n11'] + contingency_table_dict['n10'] - corrected_ocp * n,
            'n01': contingency_table_dict['n11'] + contingency_table_dict['n01'] - corrected_ocp * n, 'n00': contingency_table_dict['n00'] - contingency_table_dict['n11'] + corrected_ocp * n}


def get_upperbound_corrected_contingency_table_dict(contingency_table_dict, target_p_value, delta=0.0001):
    n = contingency_table_dict['n11'] + contingency_table_dict['n10'] + contingency_table_dict['n01'] + contingency_table_dict['n00']
    ocp = contingency_table_dict['n11'] / n
    corrected_ocp = ocp
    if (ocp != 0) & (ocp != 1):
        bound_dict = bound_dict_for_likelihood_ratio_test_with_binomial_distribution(ocp, n, target_p_value, delta)
        corrected_ocp = bound_dict['upperbound']
    return {'n11': corrected_ocp*n, 'n10': contingency_table_dict['n11'] + contingency_table_dict['n10'] - corrected_ocp * n,
            'n01': contingency_table_dict['n11'] + contingency_table_dict['n01'] - corrected_ocp * n, 'n00': contingency_table_dict['n00'] - contingency_table_dict['n11'] + corrected_ocp * n}
