import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

result_df = pd.read_excel('data/real/AKI/summary.xlsx')
target_type_list = sorted(list(set(result_df['Method'])))
#'''
for target_type in target_type_list:
    target_df = result_df[result_df['Method'] == target_type]
    target_ci_df = target_df[target_df['Modification'] == 'CIL']
    target_ecc_df = target_df[target_df['Modification'] == 'REC']
    plt.figure(figsize=(6, 4.5))
    or_y = float(target_df[target_df['Modification'] == 'AOR']['RQS'])
    cc_y = float(target_df[target_df['Modification'] == 'ACC']['RQS'])
    ecc_x = np.log10(np.array(list(target_ecc_df['Alpha'])+[1]))
    ecc_y = np.array(list(target_ecc_df['RQS'])+[or_y])
    cil_x = np.log10(np.array(list(target_ci_df['Alpha'])+[1]))
    cil_y = np.array(list(target_ci_df['RQS'])+[or_y])
    print(target_type)
    plt.ylim(0.3, 0.8)
    plt.plot(ecc_x, ecc_y, color='black', linestyle='-', marker='o', markersize=4)
    plt.plot(cil_x, cil_y, color='black', linestyle='--', marker='o', markersize=4)
    plt.hlines(cc_y, min(ecc_x), max(ecc_x), color='black', linestyle='-.')
    plt.hlines(or_y, min(ecc_x), max(ecc_x), color='black', linestyle=':')
    plt.legend(['ECC (Our Method)', 'MLE Lower Bound', 'Continuity Correction', 'MLE'])
    plt.show()
'''
best_result_group = result_df.groupby(['Method', 'Modification'])
best_result = best_result_group['RQS'].max()
types = ['AV', 'LV', 'OR', 'PR', 'RR']
rdcg_dict = {}
rdcg_dict['MLE'] = (best_result['AV']['AOR'], best_result['LV']['AOR'], best_result['OR']['AOR'], best_result['PR']['AOR'], best_result['RR']['AOR'])
rdcg_dict['MLE Lower Bound'] = (best_result['AV']['CIL'], best_result['LV']['CIL'], best_result['OR']['CIL'], best_result['PR']['CIL'], best_result['RR']['CIL'])
rdcg_dict['Continuity Correction'] = (best_result['AV']['ACC'], best_result['LV']['ACC'], best_result['OR']['ACC'], best_result['PR']['ACC'], best_result['RR']['ACC'])
rdcg_dict['ECC (Our Method)'] = (best_result['AV']['REC'], best_result['LV']['REC'], best_result['OR']['REC'], best_result['PR']['REC'], best_result['RR']['REC'])
rdcg_dict['BCPNN'] = (0, 0, 0, best_result['BCPNN']['AOR'], 0)
x = np.arange(len(types))
width = 0.12
multiplier = 0
fig, ax = plt.subplots(layout='constrained')
for type, rdcg in rdcg_dict.items():
    offset = width * multiplier
    rects = ax.bar(x+offset, rdcg, width, label=type)
    #ax.bar_label(rects, padding=3)
    multiplier += 1
ax.set_ylabel('RDCG')
types_name = ['Added Value', 'Leverage', 'Odds Ratio', 'Probability Ratio', 'Relative Risk']
ax.set_xticks(x + width, types_name)
ax.legend(loc='upper left', ncols=5)
ax.set_ylim(0, 0.8)
plt.show()
#'''
