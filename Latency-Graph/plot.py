import matplotlib.pyplot as plt
import numpy as np
import math
import csv

x = []
y = []

with open('output.csv', 'r') as csvfile:
    idx = []
    for row in csv.reader(csvfile, delimiter=','):
        idx.append(int(row[0]))
        x.append(float(row[1]))
        y.append(float(row[2]))


 
# data to plot
n_groups = len(x)
means_frank = x
means_guido = y
 
# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8
 
rects1 = plt.bar(index, means_frank, bar_width,
                 alpha=opacity,
                 color='#0288D1',
                 label='Client-KDC Latency')
 
rects2 = plt.bar(index + bar_width, means_guido, bar_width,
                 alpha=opacity,
                 color='#D81B60',
                 label='Client-Client Latency')
 
plt.xlabel('Round')
plt.ylabel('Latency in ms')
plt.title('Needham-Schroeder-Protocol')
plt.xticks(index + bar_width, idx)
plt.legend()
 
plt.tight_layout()
plt.show()