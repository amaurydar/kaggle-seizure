__author__ = 'amaury'

import json
import os
import scipy.io
import numpy as np


class Segment(object):
    def __init__(self, data, duration, time_to_seizure, origin):
        self.data = data
        self.duration = np.float32(duration)
        self.time_to_seizure = np.float32(time_to_seizure)
        self.origin = origin

    def __str__(self):
        return ('Origin : %s \n' % str(self.origin) +
                'Data shape : %s \n' % str(self.data.shape) +
                'Duration : %s \n' % self.duration +
                'Time to seizure : %s' % self.time_to_seizure)

    def subSegment(self, start, length):
        if (0 <= start) & (start < self.data.shape[1]) & (start + length <= self.data.shape[1]):
            return Segment(self.data[:, start:(start + length)],
                           self.duration * (float(length) - 1) / (float(self.data.shape[1]) - 1),
                           self.time_to_seizure - self.duration * float(start) / (float(self.data.shape[1]) - 1),
                           (self.origin[0], self.origin[1], self.origin[2], self.origin[3] + start))
        else:
            raise Exception("incorrect subsegment bounds")

    def subSegments(self, duration, step):
        if duration <= self.duration:
            duration_length = int(duration / self.duration * (self.data.shape[1] - 1))
            step_length = int(step / self.duration * (self.data.shape[1] - 1))
            print 'Duration, Step of the yielded segments is : %s, %s' % (
                (float(duration_length) - 1) / (self.data.shape[1] - 1) * self.duration,
                (float(step_length) - 1) / (self.data.shape[1] - 1) * self.duration)
            for i in xrange(int(float(self.data.shape[1] - duration_length) / step_length) + 1):
                yield self.subSegment(i * step_length, duration_length)
        else:
            raise Exception("incorrect subsegments duration")


class Subject(object):
    def __init__(self, race, n):
        self.race = race
        self.n = n
        with open('SETTINGS.json') as f:
            settings = json.load(f)
        self.dir = str(settings['data-dir']) + '/%s_%s' % (self.race, self.n)
        if race == 'Dog':
            self.inter_time_to_seizure = np.float32(settings['dog_inter_time_to_seizure'])  # 1semaine
            self.pre_time_to_seizure = np.float32(settings['dog_pre_time_to_seizure'])  # 5min
        elif race == 'Patient':
            self.inter_time_to_seizure = np.float32(settings['patient_inter_time_to_seizure'])  # 4h
            self.pre_time_to_seizure = np.float32(settings['patient_pre_time_to_seizure'])  # 5min
        else:
            raise Exception("incorrect race")


    def hourSegments(self, type):
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
                    if i == 0:
                        raise Exception("file %s not found" % filename)
                    done = True

            if not done:
                if type == 'preictal':
                    time_to_seizure = self.pre_time_to_seizure
                elif type == 'interictal':
                    time_to_seizure = self.inter_time_to_seizure
                elif type == 'test':
                    time_to_seizure = None
                else:
                    raise Exception("incorrect data in file %s" % filename)

                origin = (self.race, self.n, i, 0)

                yield Segment(data, duration, time_to_seizure, origin)

                i += 1