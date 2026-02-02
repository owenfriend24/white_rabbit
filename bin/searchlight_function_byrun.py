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

       # print(f'shape: {dsm.shape}')
       # print(f'range: {dsm.min()} - {dsm.max()}')

        ### calculate the difference to determine representational change ###
        eps = 1e-7
        dsm_z = numpy.arctanh(numpy.clip(dsm, -1 + eps, 1 - eps))

        ### set up the vectors to hold the sorted data ###
        same_context = []
        diff_context = []
        # compute contrast

        ### loop through the data to sort the within and across comparisons ###
        n = len(dsm_z)

        for x in range(n):
            for y in range(x + 1, n):
                dstmp = dsm_z[x, y]
                if dataset.sa['run'][x] == dataset.sa['run'][y]:  # only do WITHIN run comparisons
                    #print(f'comparing within run {dataset.sa["run"][x]}')
                    if dataset.sa['mini_block'][x] == dataset.sa['mini_block'][y]:  # trials WITHIN a mini block
                        #print(f'comparing within mini block: {dataset.sa["mini_block"][x]}')
                        if dataset.sa['item'][x] != dataset.sa['item'][y]:
                           #print(f'comparing two trials: {dataset.sa["item"][x]} vs {dataset.sa["item"][y]}')
                            if dataset.sa['context'][x] + dataset.sa['context'][y] == 2:
                                #print(f'SAME context: similarity = {dstmp}')
                                same_context.append(dstmp)
                            else:
                                diff_context.append(dstmp)
                                #print(f'DIFFERENT context: similarity = {dstmp}')
                # else:
                #     print(f'NOT comparing run {dataset.sa["run"][x]} to {dataset.sa["run"][y]}')

        #### convert items to arrays ###
        same_context = numpy.array(same_context)
        diff_context = numpy.array(diff_context)

        #print(f'same context: shape = {same_context.shape}, min = {same_context.min()}, max = {same_context.max()}')

        #print(f'diff context: shape = {diff_context.shape}, min = {diff_context.min()}, max = {diff_context.max()}')


        same_over_diff = numpy.nanmean(same_context) - numpy.nanmean(diff_context)
        #print(f'same over diff: {same_over_diff}')

        # contrast conditions
        return numpy.array([same_over_diff], dtype=numpy.float32)
