import matplotlib.pyplot as plt
import math
import api.analytics.descriptive.distribution.conversion_between_p_value_and_statistic_score as aaddcbpvass

x = []
y = []
z = []
k = 40
n = 100
for i in range(1, 100):
    v = i/100
    lr = -2*(k*math.log(v)+(n-k)*math.log(1-v)-k*math.log(k/n)-(n-k)*math.log(1-k/n))
    p = aaddcbpvass.get_p_value_from_chi_square(lr, 1)
    x.append(v)
    y.append(lr)
    z.append(p)
plt.figure(figsize=(6, 4.5))
plt.plot(x, z, c='black')
plt.xlabel('$P(D_i, A_p)$')
plt.ylabel('Significance Level')
plt.show()
