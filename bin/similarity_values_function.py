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
import pandas as pd

class similarity_values_function(Measure):

    def __init__(self, metric, output, comp):
        Measure.__init__(self)

        self.metric = metric
        self.comp = comp
        self.dsm = []
        self.output = output

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

        ### loop through the data to sort the within and across comparisons ###
        n = len(dsm_z)

        # set up a DATAFRAME to hold the sorted data
        df = pd.DataFrame(columns = ['comparison', 'run_1', 'mini_block_1', 'item_1', 'run_2', 'mini_block_2', 'item_2', 'pattern_similarity'])

        ### loop through the data to sort the within and across comparisons ###
        for x in range(n):

            for y in range(x + 1, n):
                dstmp = dsm_z[x, y]
                if dataset.sa['run'][x] == dataset.sa['run'][y]:  # only do WITHIN run comparisons
                    #print(f'comparing within run {dataset.sa["run"][x]}')
                    if dataset.sa['mini_block'][x] == dataset.sa['mini_block'][y]:  # trials WITHIN a mini block
                        #print(f'comparing within mini block: {dataset.sa["mini_block"][x]}')
                        if dataset.sa['item'][x] != dataset.sa['item'][y]:
                           #print(f'comparing two trials: {dataset.sa["item"][x]} vs {dataset.sa["item"][y]}')
                            if dataset.sa['context'][x] + dataset.sa['context'][y] == 0:
                                #print(f'SAME context: similarity = {dstmp}')
                                df.loc[len(df)] = ['same_context', dataset.sa['run'][x], dataset.sa['mini_block'][x], dataset.sa['item'][x],
                                               dataset.sa['run'][y], dataset.sa['mini_block'][y], dataset.sa['item'][y], dstmp]
                            else:
                                df.loc[len(df)] = ['different_context', dataset.sa['run'][x], dataset.sa['mini_block'][x],
                                                   dataset.sa['item'][x],
                                                   dataset.sa['run'][y], dataset.sa['mini_block'][y],
                                                   dataset.sa['item'][y], dstmp]
                                #print(f'DIFFERENT context: similarity = {dstmp}')
                # else:
                #     print(f'NOT comparing run {dataset.sa["run"][x]} to {dataset.sa["run"][y]}')

        return df
        
        