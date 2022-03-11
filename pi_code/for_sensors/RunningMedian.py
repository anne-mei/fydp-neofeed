import numpy as np
import math
from collections import deque
class RunningMedian:
    def __init__(self,window_size):
        self.window_size = window_size
        self.values = []
        self.sortIdx = []
        self.filtered_values = []
        self.values_sorted = []
    def qsort(self,inlist):
        if inlist == []: 
            return []
        else:
            pivot = inlist[0]
            lesser = self.qsort([x for x in inlist[1:] if x < pivot])
            greater = self.qsort([x for x in inlist[1:] if x >= pivot])
            return lesser + [pivot] + greater
    def add(self,val):
        self.values.append(val)
        if len(self.values)>self.window_size:
            self.values.pop(0)


    def findAvgMedian(self,mean_size):
        self.values_sorted = self.qsort(self.values)
        
        if len(self.values_sorted)<mean_size:
            return np.mean(self.values_sorted)
        else:
            median = math.floor(len(self.values_sorted)/2)
            half_mean_size = math.floor(mean_size/2)
            start_indx = median-half_mean_size
            end_indx = median+half_mean_size
            return np.mean(self.values_sorted[start_indx:end_indx])