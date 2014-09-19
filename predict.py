__author__ = 'amaury'
from common import data
from common import transforms
import sklearn.ensemble
import pickle
import numpy as np
import os
import scipy.io
from common import data

model = pickle.load(open('model.p', 'r'))

dog_1 = data.Subject('Dog', 1)

text_file = open("submission.txt", "w")
text_file.write("clip,preictal")
text_file.write("\n")

done = False
i = 1
while not done:
    filepath = '%s/%s_%s_%s_segment_%04d.mat' % (dog_1.dir, dog_1.race, dog_1.n, 'test', i)
    filename = '%s_%s_%s_segment_%04d.mat' % (dog_1.race, dog_1.n, 'test', i)
    print filename
    if os.path.exists(filepath):
        text_file.write("%s,%s" % (filename, 0))
        text_file.write("\n")

        mat = scipy.io.loadmat(filepath)
        name = None
        for a in mat.keys():
            if not '__' in a:
                name = a
        duration = mat[name][0][0][1][0][0]
        data_ = mat[name][0][0][0]
        fullSegment = data.Segment(data_, duration, None, ('Dog', 1, 'test', 0))
        X = []
        for segment in fullSegment.subSegments(1, 1):
            fft = transforms.FFT()
            mag = transforms.Magnitude()
            x = mag.apply(fft.apply(segment.data))
            x = np.array([w[:60] for w in x])

            x = x.flatten()

            X.append(x.astype(np.float32))
        X = np.array(X)
        print model.feature_importances_
        pred = model.predict_proba(X)
        print pred


    else:
        done = True
    i += 1

print pred

text_file.close()
