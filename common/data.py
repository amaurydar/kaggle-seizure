__author__ = 'amaury'

import json
import os
import scipy.io
import numpy as np


class Segment(object):
    def __init__(self, data, duration, time_to_seizure):
        self.data = data
        self.duration = duration
        self.time_to_seizure = time_to_seizure

    def __str__(self):
        return ('Data shape : %s \n' % str(self.data.shape) +
                'Duration : %s \n' % self.duration +
                'Time to seizure : %s' % self.time_to_seizure)

    def subsegment(self, start, length):
        if (0 <= start) & (start < self.data.shape[1]) & (start + length <= self.data.shape[1]):
            return Segment(self.data[:, start:(start + length)],
                           self.duration * (float(length) - 1) / (float(self.data.shape[1]) - 1),
                           self.time_to_seizure - self.duration * float(start) / (float(self.data.shape[1]) - 1))
        else:
            raise Exception("incorrect subsegment bounds")


class Subject(object):
    def __init__(self, race, n):
        self.race = race
        self.n = n
        with open('SETTINGS.json') as f:
            settings = json.load(f)
        self.dir = str(settings['data-dir']) + '/%s_%s' % (self.race, self.n)
        if race == 'Dog':
            self.inter_time_to_seizure = float(604800)  # 1semaine
            self.pre_time_to_seizure = float(300)  # 5min
        elif race == 'Patient':
            self.inter_time_to_seizure = float(14400)  # 4h
            self.pre_time_to_seizure = float(300)  # 5min
        else:
            raise Exception("incorrect race")

    def hour_segments(self, type):
        done = False
        i = 0
        while not done:
            duration = float(0)
            data = None
            for j in xrange(6):
                filename = '%s/%s_%s_%s_segment_%04d.mat' % (self.dir, self.race, self.n, type, i * 6 + j + 1)
                if os.path.exists(filename):
                    mat = scipy.io.loadmat(filename)
                    name = None
                    for a in mat.keys():
                        if not '__' in a:
                            name = a
                    duration += mat[name][0][0][1][0][0]
                    if data is None:
                        data = mat[name][0][0][0]
                    else:
                        data = np.concatenate((data, mat[name][0][0][0]), axis=1)
                else:
                    if i == 1:
                        raise Exception("file %s not found" % filename)
                    done = True

            if not done:
                if type == 'preictal':
                    time_to_seizure = self.pre_time_to_seizure + float(3600)
                elif type == 'interictal':
                    time_to_seizure = self.inter_time_to_seizure + float(3600)
                elif type == 'test':
                    time_to_seizure = None
                else:
                    raise Exception("incorrect data in file %s" % filename)

                yield Segment(data, duration, time_to_seizure)

                i += 1

    def segments(self, type, duration):
        for hour_segment in self.hour_segments(type):
            length = round(duration / hour_segment.duration * hour_segment.data.shape[1])
            break

        print 'Duration of the yielded segments is : %s' % (
            (length - 1) / (hour_segment.data.shape[1] - 1) * hour_segment.duration)

        for hour_segment in self.hour_segments(type):
            i = 0
            while i + length <= hour_segment.data.shape[1]:
                yield hour_segment.subsegment(i, length)
                i += length