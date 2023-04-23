
def get_target_input_value(target_output_value, monotonic_function, target_input_value_upperbound, target_input_value_lowerbound, other_parameter_dict, delta, whether_manual_monotonic=False, whether_manual_increase=True):
    target_input_value_middle = (target_input_value_upperbound + target_input_value_lowerbound) / 2
    if whether_manual_monotonic:
        whether_increase = whether_manual_increase
    else:
        whether_increase = True
        if monotonic_function(target_input_value_upperbound, other_parameter_dict) < monotonic_function(target_input_value_lowerbound, other_parameter_dict):
            whether_increase = False
    while abs(monotonic_function(target_input_value_middle, other_parameter_dict) - target_output_value) > delta:
        if whether_increase:
            if monotonic_function(target_input_value_middle, other_parameter_dict) > target_output_value:
                target_input_value_upperbound = target_input_value_middle
            else:
                target_input_value_lowerbound = target_input_value_middle
        else:
            if monotonic_function(target_input_value_middle, other_parameter_dict) > target_output_value:
                target_input_value_lowerbound = target_input_value_middle
            else:
                target_input_value_upperbound = target_input_value_middle
        target_input_value_middle = (target_input_value_upperbound + target_input_value_lowerbound) / 2
    return target_input_value_middle
