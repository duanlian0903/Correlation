import api.operation.common.data_type.file_operation as aocdtfo

json_result = aocdtfo.load_json_file_as_dict('data/AKI/rsq.json')
base_method_list = ['CS', 'LR', 'BCPNN']
correlation_method_list = ['AV', 'LV', 'OR', 'PR', 'RR']
correction_type_list = ['CIC', 'REC']

check = 1