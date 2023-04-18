import math


def likelihood_ratio_score_for_binomial_distribution(observed_prob, null_prob, n):
    likelihood_ratio_score = math.inf
    if (observed_prob != 0) & (observed_prob != 1):
        if (null_prob != 0) & (null_prob != 1):
            likelihood_ratio_score = - 2 * n * (1 - observed_prob) * math.log((1-null_prob)/(1-observed_prob)) - 2 * n * observed_prob * math.log(null_prob/observed_prob)
        else:
            likelihood_ratio_score = math.inf
    return likelihood_ratio_score
