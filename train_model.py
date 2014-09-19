__author__ = 'amaury'

__author__ = 'amaury'
from common import data
from common import transforms
import sklearn.ensemble
import pickle
import numpy as np

X_train = pickle.load(open('X_train.p', 'r'))
y_train = pickle.load(open('y_train.p', 'r'))

model = sklearn.ensemble.RandomForestClassifier(n_estimators=50,
                                                n_jobs=-1,
                                                verbose=3)

model.fit(X_train, y_train)

pickle.dump(model, open('model.p', 'wb'))

