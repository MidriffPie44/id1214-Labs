from sklearn import tree
import csv

with open('data.csv', newline='') as f:
    reader = csv.reader(f)
    raw = list(reader)


data = []
labels = []
for raw_datapoint in raw[1:]: # every data point in the raw data ignoring the table header
    datapoint = [
        raw_datapoint[1], # price
        raw_datapoint[2], # bedrooms
        raw_datapoint[4], # sqft_living
        raw_datapoint[5], # sqft_lot
        raw_datapoint[6], # floors
        raw_datapoint[9], # condition
        raw_datapoint[13], # year built
    ]
    datapoint = [round(float(entry)) for entry in datapoint] # make all entries integers
    labels.append(round(float(raw_datapoint[3]))) # number of bathrooms (independent variable)

    data.append(datapoint)

preidction_data = data[:len(data)//10]          # use 10% of data for predictions
preidction_labels = labels[:len(labels)//10]    # use 10% of data for predictions

training_data = data[len(data)//10:]            # use the remaining 90% for training
training_labels = labels[len(labels)//10:]      # use the remaining 90% for training

clf = tree.DecisionTreeClassifier()
clf.fit(training_data, training_labels)

predictions = clf.predict(preidction_data)

correct_predictions = 0
for i in range(len(predictions)):
    if preidction_labels[i] == predictions[i]:
        correct_predictions += 1

print(correct_predictions, len(predictions), 100*correct_predictions/len(predictions), '%')




