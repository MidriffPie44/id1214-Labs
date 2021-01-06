import csv
import matplotlib.pyplot as plt

import data_plot

layers = []

y = [57.45, 60.14, 60.14, 61.22, 60.44, 60.44]
x = [0,1,2,3,4,5]

data_plot.plot_accuracy(x, y, x_label='Number of hidden layers', y_label='Model Accuracy')

quit()


with open('data.csv', newline='') as f:
    reader = csv.reader(f)
    data_id = []
    duration = []
    for match in list(reader)[1:]:
        match = [int(data_point) for data_point in match]
        data_id.append(match[0])
        duration.append(match[-3])

with open('evaluation.csv', newline='') as f:
    reader = csv.reader(f)
    data_id_eval = []
    duration_eval = []
    for match in list(reader)[1:]:
        match = [int(data_point) for data_point in match]
        data_id_eval.append(match[0])
        duration_eval.append(match[-3])
        
intersection = []
for match in data_id:
    if match in data_id_eval:
        intersection.append(match)
    
print(intersection)
print(len(intersection))
    
quit()

set_y = [0]*(max(duration)+1)

max_index = duration.index(max(duration))
print(data_id[max_index])

for match_duration in duration:
    set_y[match_duration] += 1

plt.plot([i/60 for i in range(len(set_y))], set_y)
plt.xlabel('x_label')
plt.ylabel('y_label')
plt.show()