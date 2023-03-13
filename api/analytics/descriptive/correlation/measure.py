import math
import api.analytics.descriptive.distribution.conversion_between_p_value_and_statistic_score as aaddcbpvass
import scipy.stats as ss
import numpy as np


def whether_within_probability_range(prob):
    if (prob >= 0) & (prob <= 1):
        return True
    else:
        return False


def get_tcp_confidence_interval(tcp, n, alpha):
    if whether_within_probability_range(tcp) & whether_within_probability_range(alpha):
        z_score = aaddcbpvass.get_z_score_from_p_value(alpha / 2)
        se = (tcp*(1-tcp)/n) ** 0.5
        return [max(0, tcp-z_score*se), min(1, tcp+z_score*se)]
    else:
        return [math.nan, math.nan]


def get_probability_ratio(tcp, ecp):
    probability_ratio = 1
    if (ecp != 0) & whether_within_probability_range(tcp) & whether_within_probability_range(ecp):
        probability_ratio = tcp / ecp
    return probability_ratio


def get_probability_ratio_confidence_interval(tcp, ecp, n, alpha):
    tcp_confidence_interval = get_tcp_confidence_interval(tcp, n, alpha)
    return [get_probability_ratio(tcp_confidence_interval[0], ecp), get_probability_ratio(tcp_confidence_interval[1], ecp)]


def get_bcpnn(tcp, ecp, n, cc=0.5):
    return get_probability_ratio(tcp + cc / n, ecp + cc / n)


def get_probability_difference(tcp, ecp):
    probability_difference = 0
    if whether_within_probability_range(tcp) & whether_within_probability_range(ecp):
        probability_difference = tcp - ecp
    return probability_difference


def get_probability_difference_confidence_interval(tcp, ecp, n, alpha):
    tcp_confidence_interval = get_tcp_confidence_interval(tcp, n, alpha)
    return [get_probability_difference(tcp_confidence_interval[0], ecp), get_probability_difference(tcp_confidence_interval[1], ecp)]


# begin of not frequent measure
def get_probability_difference_ratio_on_tcp(tcp, ecp, power_number=1.0):
    probability_difference_ratio = -math.inf
    if tcp != 0:
        probability_difference_ratio = get_probability_difference(tcp, ecp) / (tcp ** power_number)
    return probability_difference_ratio


def get_probability_difference_ratio_on_tcp_with_continuity_correction(tcp, ecp, n, cc=0.5, power_number=1.0):
    return get_probability_difference_ratio_on_tcp(tcp + cc / n, ecp + cc / n, power_number)


def get_probability_difference_ratio_on_ecp(tcp, ecp, power_number=1.0):
    # power_number can be 1/itemset_size to adjust.
    probability_difference_ratio = 0
    if ecp != 0:
        probability_difference_ratio = get_probability_difference(tcp, ecp) / (ecp ** power_number)
    return probability_difference_ratio


def get_probability_difference_ratio_on_ecp_with_continuity_correction(tcp, ecp, n, cc=0.5, power_number=1.0):
    return get_probability_difference_ratio_on_ecp(tcp + cc / n, ecp + cc / n, power_number)
# end of not frequent measure


def get_two_way_support(tcp, ecp):
    two_way_support = 0
    if whether_within_probability_range(tcp) & whether_within_probability_range(ecp):
        if ecp != 0:
            if tcp == 0:
                two_way_support = 0
            else:
                two_way_support = tcp * math.log(tcp / ecp)
    return two_way_support


def get_likelihood_ratio(tcp, ecp, n):
    likelihood_ratio = 0
    if (ecp != 0) & (ecp != 1):
        delta = 0.0001
        if tcp == 0:
            tcp = delta / n
        if tcp == 1:
            tcp = 1 - delta / n
        likelihood_ratio = tcp * n * math.log(tcp / ecp) + (1 - tcp) * n * math.log((1 - tcp) / (1 - ecp))
        if tcp < ecp:
            likelihood_ratio = -likelihood_ratio
    return likelihood_ratio


def get_chi_square(tcp, ecp, n):
    chi_square = 0
    if ecp != 0:
        chi_square = n * (tcp - ecp) * (tcp - ecp) / ecp
        if tcp < ecp:
            chi_square = -chi_square
    return chi_square


def get_added_value(contingency_table_dict):
    try:
        return contingency_table_dict['n11'] / (contingency_table_dict['n11'] + contingency_table_dict['n10']) - (contingency_table_dict['n11'] + contingency_table_dict['n01']) / (contingency_table_dict['n11'] + contingency_table_dict['n10'] + contingency_table_dict['n01'] + contingency_table_dict['n00'])
    except:
        return 0


def get_added_value_confidence_interval(contingency_table_dict, alpha):
    z_score = aaddcbpvass.get_z_score_from_p_value(alpha / 2)
    try:
        n1 = contingency_table_dict['n11'] + contingency_table_dict['n10']
        n2 = contingency_table_dict['n11'] + contingency_table_dict['n10'] + contingency_table_dict['n01'] + contingency_table_dict['n00']
        p1 = contingency_table_dict['n11'] / n1
        p2 = (contingency_table_dict['n11'] + contingency_table_dict['n01']) / n2
        # se = (p1*(1-p1)/n1+p2*(1-p2)/n2) ** 0.5
        se = (p1*(1-p1)/n1) ** 0.5
        return [p1-p2-z_score*se, p1-p2+z_score*se]
    except:
        return [0, 0]


def get_relative_risk(contingency_table_dict):
    try:
        return (contingency_table_dict['n11'] * (contingency_table_dict['n01'] + contingency_table_dict['n00'])) / (contingency_table_dict['n01'] * (contingency_table_dict['n11'] + contingency_table_dict['n10']))
    except:
        return 1


def get_relative_risk_confidence_interval(contingency_table_dict, alpha):
    z_score = aaddcbpvass.get_z_score_from_p_value(alpha / 2)
    try:
        se = (contingency_table_dict['n10'] / ((contingency_table_dict['n11'] + contingency_table_dict['n10']) * contingency_table_dict['n11']) + contingency_table_dict['n00'] / ((contingency_table_dict['n01'] + contingency_table_dict['n00']) * contingency_table_dict['n01'])) ** 0.5
        rr = get_relative_risk(contingency_table_dict)
        return [rr/math.exp(z_score*se), rr*math.exp(z_score*se)]
    except:
        return [1, 1]


def get_odds_ratio(contingency_table_dict):
    try:
        return (contingency_table_dict['n11'] * contingency_table_dict['n00']) / (contingency_table_dict['n10'] * contingency_table_dict['n01'])
    except:
        return 1


def get_odds_ratio_confidence_interval(contingency_table_dict, alpha):
    z_score = aaddcbpvass.get_z_score_from_p_value(alpha / 2)
    try:
        se = (1/contingency_table_dict['n11']+1/contingency_table_dict['n10']+1/contingency_table_dict['n01']+1/contingency_table_dict['n00']) ** 0.5
        odds_ratio = get_odds_ratio(contingency_table_dict)
        return [odds_ratio/math.exp(z_score*se), odds_ratio*math.exp(z_score*se)]
    except:
        return [1, 1]


def get_correlation_degree_confidence_interval_point_estimation(correlation_degree_confidence_interval, independent_value):
    point_estimation = independent_value
    if independent_value < correlation_degree_confidence_interval[0]:
        point_estimation = correlation_degree_confidence_interval[0]
    elif independent_value > correlation_degree_confidence_interval[1]:
        point_estimation = correlation_degree_confidence_interval[1]
    return point_estimation


def get_phi_coefficient(contingency_table_dict):
    try:
        return (contingency_table_dict['n11'] * contingency_table_dict['n00'] - contingency_table_dict['n10'] * contingency_table_dict['n01']) / math.sqrt((contingency_table_dict['n11'] + contingency_table_dict['n10']) * (contingency_table_dict['n01'] + contingency_table_dict['n00']) * (contingency_table_dict['n10'] + contingency_table_dict['n00']) * (contingency_table_dict['n11'] + contingency_table_dict['n01']))
    except:
        return 0


def get_phi_coefficient_confidence_interval(contingency_table_dict, alpha):
    try:
        r = get_phi_coefficient(contingency_table_dict)
        n = contingency_table_dict['n11'] + contingency_table_dict['n00'] + contingency_table_dict['n10'] + contingency_table_dict['n01']
        # we use Fisher transformation
        r_z = np.arctanh(r)
        se = 1/np.sqrt(n-3)
        z = ss.norm.ppf(1-alpha/2)
        lo_z, hi_z = r_z-z*se, r_z+z*se
        lo, hi = np.tanh((lo_z, hi_z))
        return [lo, hi]
    except:
        print(contingency_table_dict, get_phi_coefficient(contingency_table_dict))
        return [0, 0]


def get_conviction(contingency_table_dict):
    try:
        return ((contingency_table_dict['n11'] + contingency_table_dict['n10']) * (contingency_table_dict['n10'] + contingency_table_dict['n00'])) / ((contingency_table_dict['n11'] + contingency_table_dict['n10'] + contingency_table_dict['n01'] + contingency_table_dict['n00']) * contingency_table_dict['n10'])
    except:
        return 1


def get_pair_correlation_type_list():
    return ["Added Value", "Relative Risk", "Odds Ratio", "Phi Coefficient", "Conviction"]


def get_itemset_correlation_degree_type_list():
    return ["Probability Ratio", "BCPNN", "Probability Difference", "Probability Difference Ratio on tcp",
            "Probability Difference Ratio on tcp with Continuity Correction",
            "Probability Difference Ratio on ecp", "Probability Difference Ratio on ecp with Continuity Correction",
            "Two-way Support"]


def get_itemset_correlation_null_hypothesis_type_list():
    return ["Likelihood Ratio", "Chi-square"]


def get_itemset_correlation_type_list():
    return get_itemset_correlation_degree_type_list() + get_itemset_correlation_null_hypothesis_type_list()


def get_correlation_score_only_for_pair(contingency_table_dict, correlation_type):
    if correlation_type == "Added Value":
        return get_added_value(contingency_table_dict)
    elif correlation_type == "Relative Risk":
        return get_relative_risk(contingency_table_dict)
    elif correlation_type == "Odds Ratio":
        return get_odds_ratio(contingency_table_dict)
    elif correlation_type == "Phi Coefficient":
        return get_phi_coefficient(contingency_table_dict)
    elif correlation_type == "Conviction":
        return get_conviction(contingency_table_dict)
    else:
        return None


def get_correlation_score_for_itemset(tcp, ecp, n, itemset_size, correlation_type, cc=0.5):
    if correlation_type == "Probability Ratio":
        return get_probability_ratio(tcp, ecp)
    elif correlation_type == "BCPNN":
        return get_bcpnn(tcp, ecp, n, cc)
    elif correlation_type == "Probability Difference":
        return get_probability_difference(tcp, ecp)
    elif correlation_type == "Probability Difference Ratio on tcp":
        return get_probability_difference_ratio_on_tcp(tcp, ecp)
    elif correlation_type == "Probability Difference Ratio on tcp with Continuity Correction":
        return get_probability_difference_ratio_on_tcp_with_continuity_correction(tcp, ecp, n, cc)
    elif correlation_type == "Probability Difference Ratio on ecp":
        return get_probability_difference_ratio_on_ecp(tcp, ecp, 1 / itemset_size)
    elif correlation_type == "Probability Difference Ratio on ecp with Continuity Correction":
        return get_probability_difference_ratio_on_ecp_with_continuity_correction(tcp, ecp, n, cc)
    elif correlation_type == "Two-way Support":
        return get_two_way_support(tcp, ecp)
    elif correlation_type == "Likelihood Ratio":
        return get_likelihood_ratio(tcp, ecp, n)
    elif correlation_type == "Chi-square":
        return get_chi_square(tcp, ecp, n)
    else:
        return None


def get_pair_correlation(contingency_table_dict, correlation_type, cc=0.5):
    n = contingency_table_dict['n11'] + contingency_table_dict['n10'] + contingency_table_dict['n01'] + contingency_table_dict['n00']
    tcp = contingency_table_dict['n11'] / n
    ecp = (contingency_table_dict['n11'] + contingency_table_dict['n10']) / n * (contingency_table_dict['n11'] + contingency_table_dict['n01']) / n
    itemset_size = 2
    if correlation_type in get_itemset_correlation_type_list():
        return get_correlation_score_for_itemset(tcp, ecp, n, itemset_size, correlation_type, cc)
    elif correlation_type in get_pair_correlation_type_list():
        return get_correlation_score_only_for_pair(contingency_table_dict, correlation_type)
    else:
        return None

'''
a = get_relative_risk_confidence_interval({'n11': 9, 'n10': 41, 'n01': 20, 'n00': 29}, 0.025)
b = get_odds_ratio_confidence_interval({'n11': 7, 'n10': 10, 'n01': 6, 'n00': 57}, 0.025)
c = get_added_value_confidence_interval({'n11': 2757, 'n10': 298, 'n01': 663, 'n00': 81}, 0.025)
d = get_tcp_confidence_interval(1219/3532, 3532, 0.025)
e = get_tcp_confidence_interval(50/1000, 1000, 1)
print(d)
'''
