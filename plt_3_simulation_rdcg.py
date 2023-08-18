import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

result_df = pd.read_excel('data/simulation/adr/RR1000000.xlsx')
target_type_list = sorted(list(set(result_df['Method'])))
target_type = 'RR'
target_df = result_df[result_df['Method'] == target_type]
target_ci_df = target_df[target_df['Modification'] == 'CIL']
target_ecc_df = target_df[target_df['Modification'] == 'REC']
plt.figure(figsize=(6, 4.5))
or_y = float(target_df[target_df['Modification'] == 'AOR']['RDCG'])
cc_y = float(target_df[target_df['Modification'] == 'ACC']['RDCG'])
ecc_x = np.log10(np.array([1] + list(target_ecc_df['Alpha'])))
ecc_y = np.array([or_y] + list(target_ecc_df['RDCG']))
cil_x = np.log10(np.array([1] + list(target_ci_df['Alpha'])))
cil_y = np.array([or_y] + list(target_ci_df['RDCG']))
plt.ylim(0, 0.8)
plt.plot(ecc_x, ecc_y, color='black', linestyle='-', marker='o', markersize=4)
plt.plot(cil_x, cil_y, color='black', linestyle='--', marker='o', markersize=4)
plt.hlines(cc_y, min(ecc_x), max(ecc_x), color='black', linestyle='-.')
plt.hlines(or_y, min(ecc_x), max(ecc_x), color='black', linestyle=':')
plt.legend(['ECC (Our Method)', 'MLE Lower Bound', 'Continuity Correction', 'MLE'])
plt.show()
