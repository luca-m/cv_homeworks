# -*- coding: utf-8 -*-

__author__ = "Luca Mella"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2013/05/20 $"
__copyright__ = "Copyright (c) 2012-2013 Luca Mella"
__license__ = "CC BY-NC-SA"

""" 
HISTOGRAM and THRESHOLDING

  IPA_histoMA(inp,tones,WW)
  IPA_histo(inp,tones,type)
  IPA_IPA_histoCdf(inp,tones,type)
  IPA_histoEq(inp,tones,type)
  IPA_IPA_histoNorm(inp,tones,type)
  
  IPA_imgStreching(img)
  IPA_imgEq(img)
  
  IPA_FindThreshold(img,tones,type)
  IPA_PeakValley(histo)

NOTE: input image is loaded in grayscale

"""

import cv2
#import cv
import numpy as np
import plots

def run(inImPath,outImPath):
  # read the image as numpy matrix
  im=cv2.imread(inImPath, cv2.CV_LOAD_IMAGE_GRAYSCALE)
  ranges=[0,255]
  hsize=[256]
  channels=[0]
  print "[HISTO_OPENCV] Calculating histogram"
  hist=cv2.calcHist([im],channels,None,hsize,ranges)
  print "[HISTO_OPENCV] Normalizing histogram"
  hist_norm=np.array([0.0]*len(hist))
  hist_acc=hist.cumsum()
  hist_norm=hist/hist_acc[255] 
  #cv2.normalize(hist,hist_norm,0,255,cv2.NORM_MINMAX)
  plots.plotHist(hist,"[HISTO_OPENCV] Histogram")
  plots.plotHist(hist_norm,"[HISTO_OPENCV] Histogram normalized")
  plots.plotHist(hist_acc,"[HISTO_OPENCV] Histogram accumulated")
  plots.showPlots()
