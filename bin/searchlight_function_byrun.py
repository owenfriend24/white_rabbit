"""Dissimilarity measure"""

__docformat__ = 'restructuredtext'

import numpy
from numpy import *
from numpy.random import randint
import scipy.stats
from scipy.stats.mstats import zscore
from scipy.ndimage import convolve1d
from scipy.sparse import spdiags
from scipy.linalg import toeplitz
from mvpa2.measures.base import Measure
from mvpa2.measures import rsa


class searchlight_function_byrun(Measure):

    def __init__(self, metric, output, niter):
        Measure.__init__(self)

        self.metric = metric
        self.dsm = []
        self.output = output
        self.niter = niter

    def __call__(self, dataset):

        self.dsm = rsa.PDist( \
            square=True, \
            pairwise_metric=self.metric, \
            center_data=False)


        ### calculate the dsm separately for each phase ###
        dsm = self.dsm(dataset)
        dsm = 1 - dsm.samples

        ### calculate the difference to determine representational change ###
        dsm_z = numpy.arctanh(dsm)

        ### set up the vectors to hold the sorted data ###
        same_context = []
        diff_context = []


        ### loop through the data to sort the within and across comparisons ###
        n = len(dsm)

        for x in range(n):
            for y in range(x + 1, n):
                dstmp = dsm_z[x, y]
                if dataset.sa['run'][x] == dataset.sa['run'][y]:  # only do WITHIN run comparisons
                    if dataset.sa['mini_block'][x] == dataset.sa['mini_block'][y]:  # trials WITHIN a mini block
                        if dataset.sa['context'][x] == dataset.sa['context'][y]:
                            if dataset.sa['item'][x] != dataset.sa['item'][y]:  # different items
                                same_context.append(dstmp)
                        elif dataset.sa['context'][x] != dataset.sa['context'][y]:  # across triad
                            if dataset.sa['item'][x] != dataset.sa['item'][y]:
                                diff_context.append(dstmp)

        #### convert items to arrays ###
        same_context = array(same_context)
        diff_context = array(diff_context)

        same_over_diff = mean(same_context) - mean(diff_context)
        diff_over_same = mean(diff_context) - mean(same_context)

        # contrast conditions
        return same_over_diff
