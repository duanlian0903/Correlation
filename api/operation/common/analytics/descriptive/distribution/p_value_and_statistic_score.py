import scipy.stats as ss


def get_chi_square_p_value(chi_square_score, degree_of_freedom):
    return 1 - ss.chi2.cdf(chi_square_score, degree_of_freedom)


def get_chi_square_score(p_value, degree_of_freedom):
    return ss.chi2.ppf(1 - p_value, degree_of_freedom)


def get_normal_distribution_p_value(z_score):
    return 1 - ss.norm.cdf(z_score)


def get_normal_distribution_z_score(p_value):
    return ss.norm.ppf(1 - p_value)
