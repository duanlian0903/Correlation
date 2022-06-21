# checked
import math
import sklearn.metrics as sm
import api.operation.common.data_type.list_dict_set_tuple as aocdtldst


def get_discounted_cumulative_gain(relevance_score_list):
    discounted_cumulative_gain = 0
    if len(relevance_score_list) > 0:
        for index in range(len(relevance_score_list)):
            discounted_cumulative_gain = discounted_cumulative_gain + relevance_score_list[index]/math.log2(index+2)
    return discounted_cumulative_gain


def get_normalized_discounted_cumulative_gain(relevance_score_list):
    descending_list = aocdtldst.get_sorted_list(relevance_score_list, descending=True)
    return get_discounted_cumulative_gain(relevance_score_list)/get_discounted_cumulative_gain(descending_list)


def get_ranking_quality_score(relevance_score_list):
    descending_list = aocdtldst.get_sorted_list(relevance_score_list, descending=True)
    best_score = get_discounted_cumulative_gain(descending_list)
    ascending_list = aocdtldst.get_sorted_list(relevance_score_list, descending=False)
    worst_score = get_discounted_cumulative_gain(ascending_list)
    original_score = get_discounted_cumulative_gain(relevance_score_list)
    return (original_score-worst_score)/(best_score-worst_score)


def get_root_mean_square_error(predicted_value_list, actual_value_list):
    root_mean_square_error = 0
    if len(predicted_value_list) != len(actual_value_list):
        print('We have error for not matching list length.')
    else:
        for index in range(len(predicted_value_list)):
            root_mean_square_error = root_mean_square_error + (predicted_value_list[index]-actual_value_list[index])**2
        root_mean_square_error = (root_mean_square_error/len(predicted_value_list))**0.5
    return root_mean_square_error


def get_accuracy(y_true, y_prediction):
    return sm.accuracy_score(y_true, y_prediction)


def get_f1(y_true, y_prediction):
    return sm.f1_score(y_true, y_prediction)


def get_recall(y_true, y_prediction):
    return sm.recall_score(y_true, y_prediction)


def get_precision(y_true, y_prediction):
    return sm.precision_score(y_true, y_prediction)


def get_roc_auc_score(y_true, y_score):
    return sm.roc_auc_score(y_true, y_score)


def get_normalized_mutual_information_score(labels_true, labels_pred):
    return sm.normalized_mutual_info_score(labels_true, labels_pred)

