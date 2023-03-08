# tested
import joblib as jl


def embarrassing_parallel_process(original_function_name, value_list, number_of_jobs):  # tested
    jl.Parallel(n_jobs=number_of_jobs)(jl.delayed(original_function_name)(value) for value in value_list)
