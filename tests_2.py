__author__ = 'amaury'
from common import data
from common import transforms
import sklearn.ensemble
import pickle
import numpy as np

dog_1 = data.Subject('Dog', 1)
X_train = []
y_train = []

for type in ('preictal', 'interictal'):
    i = 0
    for hour_segment in dog_1.hourSegments(type):
        i += 1
        print type, i
        for segment in hour_segment.subSegments(1, 1):
            y_train.append(np.float32(segment.time_to_seizure <= dog_1.pre_time_to_seizure))
            fft = transforms.FFT()
            mag = transforms.Magnitude()
            x = mag.apply(fft.apply(segment.data))
            x = np.array([w[:60] for w in x])

            x = x.flatten()

            X_train.append(x.astype(np.float32))

X_train = np.array(X_train).astype(np.float32)
y_train = np.array(y_train).astype(np.float32)

pickle.dump(X_train, open('X_train.p', 'wb'))
pickle.dump(y_train, open('y_train.p', 'wb'))
