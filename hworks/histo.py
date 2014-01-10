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
import numpy as np
import plots

def run(inImPath,outImPath):
  # read the image as numpy matrix
  im=cv2.imread(inImPath, cv2.CV_LOAD_IMAGE_GRAYSCALE)
  ranges=[0, 255]
  #hsize=[256]
  #channels=[0]
  #hist=cv2.IPA_histo(im, [0], None, hsize, ranges)
  #(hist,_)=np.histogram(im,bins=256,range=ranges)
  print "[HISTO] IPA_histo"
  hist=IPA_histo(im,ranges)
  print "[HISTO] IPA_histoConvolution1D Moving Average"
  hist_avg=IPA_histoConvolution1D(hist,[1/11.0]*11)
  print "[HISTO] IPA_histoConvolution1D Gaussian"
  hist_gauss=IPA_histoConvolution1D(hist,np.array([1,2,3,4,5,4,3,2,1]))
  print "[HISTO] IPA_histoNorm"
  hist_norm=IPA_histoNorm(hist,im.size)
  print "[HISTO] IPA_histoCdf"
  hist_cdf=IPA_histoCdf(hist_norm)
  print "[HISTO] IPA_histoTransform"
  im_eq=IPA_histoTransform(im,hist_cdf)
  print "[HISTO] IPA_FindThreshold_Isodata"
  thr_isodata=IPA_FindThreshold_Isodata(hist_avg)
  print "[HISTO] IPA_Bynarize"
  im_thr_isodata=IPA_Bynarize(im,thr_isodata)
  print "[HISTO] IPA_FindThreshold_Otsu"
  thr_otsu=IPA_FindThreshold_Otsu(hist_avg)
  print "[HISTO] IPA_Bynarize"
  im_thr_otsu=IPA_Bynarize(im,thr_otsu)
  print "[HISTO] IPA_histoTransform"
  [p,v]=IPA_PeakValley(hist_gauss)

  print "Plotting.."
  plots.plotImage(im,"[HISTO] Original Image")
  plots.plotHist(hist_avg,"[HISTO] Averaged Histogram (moving average filter)")
  plots.plotHistPeakValley(hist_gauss,p,v,"Peaks and valley")
  plots.plotHist(hist_norm,"[HISTO] Normalized histogram")
  plots.plotHist(hist_cdf,"[HISTO] Cumulative histogram")
  plots.plotHist(hist,"[HISTO] Histogram (+Isodata)",thr_isodata)
  plots.plotHist(hist,"[HISTO] Histogram (+Otsu)",thr_otsu)
  plots.plotImage(im_eq,"[HISTO] Equalized Image")  
  plots.plotImage(im_thr_isodata,"[HISTO] Binarizer (Isodatata)")
  plots.plotImage(im_thr_otsu,"[HISTO] Binarizer (Otsu)")
  
  plots.showPlots()

#
# Histogram Functions
#

def IPA_histo(im, rang=[0,255]):
  """ Calculate an histogram """
  (h,b)=np.histogram(im.flatten(),bins=(rang[1]-rang[0]+1),density=False)
  return h

def IPA_histoNorm(hist,nvals=None):
  """ Normalize an histogram """
  if not type(hist) == np.array:
    hist=np.array(hist)
  if nvals is None:
    nvals=np.sum(hist)
  return hist / np.float32(nvals)

def IPA_histoConvolution1D(hist, mask):
  """ 0-padded 1D convolution """
  return np.convolve(np.array( [0.0]*(len(mask)/2)+hist.tolist()+[0.0]*(len(mask)/2)),mask,'valid')

def IPA_histoCdf(hist):
  """ histogram CDF """
  return np.cumsum(hist)

def IPA_histoTransform(im, new_histo):
  """ Histogram transformation function """
  # This is the numpy magic..
  return new_histo[im]

def IPA_Bynarize(im, threshold):
  """ Bynarize a Greyscale image (assumption: UINT8 image)"""
  th=np.array([0]*(threshold) + [1]*(255-threshold) ) 
  return th[im]

def IPA_FindThreshold(hist, type):
  """ Histogram transformation function """
  if type=='otsu':
    return IPA_FindThreshold_Otsu(hist)
  elif type=='isodata':
    return IPA_FindThreshold_Isodata(hist)

def IPA_FindThreshold_Otsu(hist):
  """ Otsu thresholding """
  if not type(hist) == np.array:
    hist=np.array(hist)
  m_sig=float("-inf")
  t_max=-1
  tot=np.sum(hist)
  sall=np.sum(np.multiply(range(len(hist)),hist))
  wb=0
  sb=0
  mb=0
  wf=0
  mf=0
  for t in range(len(hist)):
    wb+=hist[t]
    if wb==0:
      continue
    wf=tot-wb
    if wf==0:
      break
    sb+=t*hist[t]
    mb=sb/wb
    mf=(sall-sb)/wf
    # in-between
    sig=wb*wf*(mb-mf)**2 
    # in-between sigma square (unoptimized)
    # sig=np.sum( np.multiply(range(t),hist[:t]) ) * \
    #  np.sum( np.multiply(range(t,len(hist)),hist[t:]) )* \
    #  np.power( np.sum(np.multiply(range(t),hist[:t]))/np.sum(hist[:t]) - \
    #          np.sum(np.multiply(range(t,len(hist)),hist[t:]))/np.sum(hist[t:]),2)
    if sig>m_sig:
      m_sig=sig
      t_max=t
  print "[HISTO] Otsu threshold={0}".format(t_max)
  return t_max

def IPA_FindThreshold_Isodata(hist):
  """ Isodata thresholding (Unoptimized) """ 
  if not type(hist) == np.array:
    hist=np.array(hist)
  thr=np.uint8(-1)
  thr_new=np.uint8(127)
  while thr!=thr_new:
    thr=thr_new
    mb=np.sum(np.multiply(range(thr), hist[:thr]) ) / sum(hist[:thr])
    mf=np.sum(np.multiply(range(thr, len(hist)), hist[thr:]) ) / sum(hist[thr:])
    thr_new=np.uint8((mb+mf)/2)
  print "[HISTO] Isodata threshold={0}".format(thr_new)
  return thr_new

def IPA_PeakValley(hist):
  """ Peak and Valley with derivate and dumb zero-crossing"""
  if not type(hist) == np.array:
    hist=np.array(hist)
  hist_d1=IPA_histoConvolution1D(hist,[-1.0,1.0]) # first derivate of the histo
  valley=[]
  peaks=[]
  #hist_d1[np.where(hist_d1>0.0)]=1
  #hist_d1[np.where(hist_d1==0.0)]=0
  #hist_d1[np.where(hist_d1<0.0)]=-1
  for i in range(len(hist_d1)-1):
    if hist_d1[i]>0 and hist_d1[i+1]<=0:
      valley+=[i]
      print "[HISTO] Valley found at {0}".format(i)
    elif hist_d1[i]<=0 and hist_d1[i+1]>0:
      peaks+=[i]
      print "[HISTO] Peek found at {0}".format(i)
  return [peaks,valley]
