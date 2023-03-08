# tested
import pickle
import os
import shutil
import pandas as pd
import json
import api.common.message as aocm


def check_file_existence(file_name):  # tested
    if isinstance(file_name, str):
        return os.path.isfile(file_name)
    else:
        return False


def check_folder_existence(folder_name):  # tested
    if isinstance(folder_name, str):
        return os.path.isdir(folder_name)
    else:
        return False


def copy_file(source_file_path, destine_file_path):  # tested
    try:
        shutil.copy2(source_file_path, destine_file_path)
    except:
        aocm.show_exception_message('Fail to copy due to unexpected errors[' + str(source_file_path) + ', ' + str(destine_file_path) + '].')


def delete_file(file_name):  # tested
    if check_file_existence(file_name):
        os.remove(file_name)


def generate_folder_for_file(file_name):  # tested
    try:
        folder_list = file_name.split('/')[:-1]
        current_path = ''
        if ':/' in file_name:
            current_path = folder_list[0]
            folder_list = folder_list[1:]
        for folder in folder_list:
            current_path = current_path + '/' + folder
            if not check_folder_existence(current_path):
                os.mkdir(current_path)
    except:
        aocm.show_exception_message('Fail to generate the related folders due to unexpected errors.')


def delete_file_in_the_current_folder(folder_name):  # tested
    try:
        generate_folder_for_file(folder_name+'/test.txt')
        file_folder_list = os.listdir(folder_name)
        for file_folder in file_folder_list:
            file_name = folder_name+'/'+file_folder
            delete_file(file_name)
    except:
        aocm.show_exception_message('Fail to delete files in the given folder level due to unexpected errors.')


def delete_file_inside_folder(folder_name):  # tested
    try:
        delete_file_in_the_current_folder(folder_name)
        file_folder_list = os.listdir(folder_name)
        for file_folder in file_folder_list:
            path = folder_name + '/' + file_folder
            if os.path.isdir(path):
                delete_file_inside_folder(path)
    except:
        aocm.show_exception_message('Fail to delete files insider all the subfolders due to unexpected errors.')


def save_pickle_data(data, file_name, whether_save_csv=False):  # tested
    try:
        if isinstance(file_name, str):
            generate_folder_for_file(file_name)
            pickle_file = open(file_name, 'wb')
            pickle.dump(data, pickle_file)
            pickle_file.close()
            if whether_save_csv:
                if isinstance(data, pd.DataFrame):
                    data.to_csv(file_name+'.csv')
                else:
                    aocm.show_exception_message('We have trouble saving ' + str(file_name) + '.csv because the variable is not a dataframe.')
        else:
            aocm.show_exception_message('We have trouble saving ' + str(file_name) + '.csv because the file name is not a string.')
    except:
        aocm.show_exception_message('We have trouble saving ' + str(file_name) + '.csv due to unexpected errors.')


def load_pickle_data(file_name):  # tested
    pickle_data = pd.DataFrame([])
    try:
        if isinstance(file_name, str):
            if check_file_existence(file_name):
                pickle_file = open(file_name, 'rb')
                pickle_data = pickle.load(pickle_file)
                pickle_file.close()
            else:
                aocm.show_exception_message('We will return a null dataframe due to non-existing file'+str(file_name)+'.')
        else:
            aocm.show_exception_message('We will return a null dataframe because the file name is not a string.')
    except:
        aocm.show_exception_message('We will return a null dataframe due to unexpected errors.')
    return pickle_data


def load_pickle_data_dict(file_name):  # tested
    data = pd.DataFrame([])
    whether_has_file = False
    try:
        if isinstance(file_name, str):
            if check_file_existence(file_name):
                data = load_pickle_data(file_name)
                whether_has_file = True
            else:
                aocm.show_exception_message('We will return False value due to non-existing file.')
        else:
            aocm.show_exception_message('We will return False value because the file name is not a string.')
    except:
        aocm.show_exception_message('We will return False value due to unexpected errors.')
    return {'whether_has_file': whether_has_file, 'data': data}


def save_excel_file(df, file_name):  # tested
    try:
        if isinstance(file_name, str):
            if isinstance(df, pd.DataFrame):
                generate_folder_for_file(file_name)
                writer = pd.ExcelWriter(file_name+'.xlsx', engine='xlsxwriter')
                df.to_excel(writer, sheet_name='sheet1')
                workbook = writer.book
                worksheet = writer.sheets['sheet1']
                worksheet.freeze_panes(1, 1)
                worksheet.autofilter(0, 0, len(df), len(df.columns))
                header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter', 'shrink': True, 'fg_color': '#7ccbfc', 'border': 1})
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num+1, value, header_format)
                writer.save()
            else:
                aocm.show_exception_message('We have trouble saving excel file because the variable is not a dataframe.')
        else:
            aocm.show_exception_message('We have trouble saving excel file because the file name is not a string.')
    except:
        aocm.show_exception_message('We have trouble saving excel file due to unexpected errors.')


def get_item_set_from_file(file_name):  # tested
    try:
        item_list = []
        if check_file_existence(file_name):
            file = open(file_name)
            lines = file.readlines()
            for line in lines:
                item_list.append(line[:-1])
        else:
            aocm.show_exception_message('We will return an empty set due to non-existing file.')
        return set(item_list)
    except:
        aocm.show_exception_message('We will return an empty set due to unexpected errors.')
        return set()


def load_json_file_as_dict(file_name):  # tested
    try:
        if check_file_existence(file_name):
            result = json.load(open(file_name))
        else:
            aocm.show_exception_message('We will return an empty dictionary due to non-existing file.')
            result = {}
    except:
        aocm.show_exception_message('We will return an empty dictionary due to unexpected errors.')
        result = {}
    return result


def save_dict_as_json_file(dict_data, file_name):  # tested
    try:
        json.dump(dict_data, open(file_name, 'w'))
        content = open(file_name, 'r').read().replace(',', ',\n')
        open(file_name, 'w').write(content)
    except:
        aocm.show_exception_message('We have unexpected errors to save json file: ' + str(file_name))


def update_json_file(file_name, updating_dict_data):  # tested
    json_dict = load_json_file_as_dict(file_name)
    try:
        for key in updating_dict_data:
            json_dict[key] = updating_dict_data[key]
    except:
        aocm.show_exception_message('We have unexpected errors to update json file with dict ' + str(updating_dict_data))
    save_dict_as_json_file(json_dict, file_name)


def generate_summary_df_in_the_folder(folder_name):  # tested
    try:
        file_folder_list = os.listdir(folder_name)
        df_list = []
        for file_folder in file_folder_list:
            file_name = folder_name+'/'+file_folder
            if os.path.isfile(file_name):
                df_list.append(load_pickle_data(file_name))
        result = pd.DataFrame([])
        if len(df_list) > 0:
            result = pd.concat(df_list)
        return result
    except:
        aocm.show_exception_message('We will return a null dataframe due to unexpected errors to generate summary df from the folder ' + str(folder_name))
        return pd.DataFrame([])


def get_index_list(df_file_name):  # tested
    try:
        return sorted(list(set(load_pickle_data(df_file_name).index)))
    except:
        aocm.show_exception_message('We will return an empty list due to unexpected errors for the df file ' + str(df_file_name))
        return []


def save_given_source_information_df_with_overwrite(ticker, filename_function, retrieve_df_function, whether_save_csv=False):  # tested
    try:
        given_source_information_df = retrieve_df_function(ticker)
        if len(given_source_information_df) != 0:
            save_pickle_data(given_source_information_df, filename_function(ticker), whether_save_csv)
        else:
            print('Information for ' + str(ticker) + ' is not saved for the empty dataframe retrieved with ' + str(retrieve_df_function))
    except:
        aocm.show_exception_message('Information for ' + str(ticker) + ' is not updated due to unexpected errors.')


def save_given_source_information_df_without_overwrite(ticker, filename_function, retrieve_df_function, whether_save_csv=False):  # tested
    try:
        if not load_pickle_data_dict(filename_function(ticker))['whether_has_file']:
            save_given_source_information_df_with_overwrite(ticker, filename_function, retrieve_df_function, whether_save_csv)
    except:
        aocm.show_exception_message('Information for ' + str(ticker) + ' is not updated due to unexpected errors.')

