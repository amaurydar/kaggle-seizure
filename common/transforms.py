__author__ = 'amaury'

import numpy as np


class FFT:
    """
    Apply Fast Fourier Transform to the last axis.
    """

    def get_name(self):
        return "fft"

    def apply(self, data):
        axis = data.ndim - 1
        return np.fft.rfft(data, axis=axis)


class Magnitude:
    """
    Take magnitudes of Complex data
    """

    def get_name(self):
        return "mag"

    def apply(self, data):
        return np.absolute(data)