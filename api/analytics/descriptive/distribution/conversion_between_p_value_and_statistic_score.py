import scipy.stats as ss


def get_p_value_from_chi_square(chi_square_score, degree_of_freedom):
    return 1 - ss.chi2.cdf(chi_square_score, degree_of_freedom)


def get_chi_square_score_from_p_value(p_value, degree_of_freedom):
    return ss.chi2.ppf(1 - p_value, degree_of_freedom)


def get_p_value_from_z_score(z_score):
    return 1 - ss.norm.cdf(z_score)


def get_z_score_from_p_value(p_value):
    return ss.norm.ppf(1 - p_value)
