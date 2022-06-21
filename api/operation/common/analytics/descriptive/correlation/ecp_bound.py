
def get_ecp_lowerbound(ocp, itemset_size):
    return ocp**itemset_size


def get_ecp_upperbound(ocp, itemset_size):
    return ((itemset_size-1+ocp)/itemset_size)**itemset_size
