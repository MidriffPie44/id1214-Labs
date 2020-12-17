import csv
import matplotlib.pyplot as plt


with open('data.csv', newline='') as f:
    reader = csv.reader(f)
    data = []
    for match in list(reader)[1:]:
        match = [int(data_point) for data_point in match]
        data.append(match)

aaa = [0]*100
bbb = range(0,100)
for datapoint in data:
    aaa[datapoint[-2]] += 1

print(aaa)

plt.plot(bbb, aaa)
plt.show() 