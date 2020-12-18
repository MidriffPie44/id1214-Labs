import csv
import matplotlib.pyplot as plt


with open('data_old_patch.csv', newline='') as f:
    reader = csv.reader(f)
    data_id = []
    for match in list(reader)[1:]:
        match = [int(data_point) for data_point in match]
        data_id.append(match[0])


with open('evaluation_old_patch.csv', newline='') as f:
    reader = csv.reader(f)
    eval_id = []
    for match in list(reader)[1:]:
        match = [int(data_point) for data_point in match]
        eval_id.append(match[0])


bbb = []
for i in eval_id:
    if i in data_id:
        bbb.append(i)
        print(eval_id.index(i))

print(len(bbb))
print(bbb)