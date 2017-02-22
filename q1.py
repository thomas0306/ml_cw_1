# Question 1
# Kwan Hau Thomas, LEE (1650501)

# Library
import pandas as pd

# import data
df = pd.DataFrame({
    'predicted': [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0],
    'actual': [1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0]
})

# a) calculate accuracy
accuracy = len(df[df.predicted == df.actual]) / float(len(df))
print 'Accuracy: %.2f' % accuracy

# b) confusion matrix
TP = len(df[(df.predicted == 1) & (df.actual == 1)])
TN = len(df[(df.predicted == 0) & (df.actual == 0)])
FP = len(df[(df.predicted == 1) & (df.actual == 0)])
FN = len(df[(df.predicted == 0) & (df.actual == 1)])
print('TP: %d' % TP)
print('TN: %d' % TN)
print('FP: %d' % FP)
print('FN: %d' % FN)

# d) precision
precision = float(TP) / (TP + FP)
print('Precision: %.2f' % precision)

# e) recall
recall = float(TP) / (TP + FN)
print('Recall: %.2f' % recall)

# f) f1 score
f1 = float(2) * (precision * recall) / (precision + recall)
print('F1: %.2f' % f1)