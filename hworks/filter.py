# -*- coding: utf-8 -*-

__author__ = "Luca Mella"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2013/05/20 $"
__copyright__ = "Copyright (c) 2012-2013 Luca Mella"
__license__ = "CC BY-NC-SA"

""" 
IMAGE FILTERING AND EDGE DETECTION
  
  IPA_conv2(img,mask,pad_type)
  IPA_edge(img,mask,op_type)
  IPA_meanfilter(img,mask_size)
  IPA_Gfilter(img,mask_size,sigma)

"""
import cv2
import numpy as np
import morpho             # NOTE: rely on the convolution operations implemented in 'hworks.morpho'
import plots

def run(inImPath,outImPath):
  # read the image as numpy matrix
  im=cv2.imread(inImPath, cv2.CV_LOAD_IMAGE_GRAYSCALE)
  #img = Image.open(inImPath)
  #im=np.array(img)
  #img = Image.fromarray(arr)
  #img.show()
  print "DISCLAIMER: Convolution in Python is pretty SLOW.."
  print "            This does not mean that python cannot be used for this kind of computation,"
  print "            but also mean that we should use libraries like 'numpy' or 'cv' which provide"
  print "            access to native algorithm implementation (read 'C/C++') directly from python."
  print "            However, this is only a homework.."
  print "[FILTER] IPA_Gfilter"
  im_gfilt=IPA_Gfilter(im,[5,5],0.5)
  print "[FILTER] IPA_meanfilter"
  im_mean=IPA_meanfilter(im,[5,5])
  print "[FILTER] IPA_edge_roberts"
  im_roberts=IPA_edge_roberts(im)
  print "[FILTER] IPA_edge_prewitt"
  im_prewitt=IPA_edge_prewitt(im)
  print "[FILTER] IPA_edge_sobel"
  im_sobel=IPA_edge_sobel(im)
  print "Plotting.."
  plots.plotImage(im,"[FILTER] Original image")
  plots.plotImage(im_mean,"[FILTER] Mean Filter")
  plots.plotImage(im_gfilt,"[FILTER] Gaussian filter")
  plots.plotImage(4*im_roberts,"[FILTER] Roberts (4*magnification)")
  plots.plotImage(4*im_prewitt,"[FILTER] Prewitt (4*magnification)")
  plots.plotImage(4*im_sobel,"[FILTER] Sobel (4*magnification)")
  plots.showPlots()

#
# Some useful operations during the convolution phase
#
conv_op=lambda pix,mask,val: max(min(float(pix*mask+val),255.0),0.0)
conv_op_unbound=lambda pix,mask,val:pix*mask+val
sum_op=lambda a,b,:max(min(a+b,255.0),0.0)
sum_op_abs=lambda a,b,:max(min(abs(a)+abs(b),255.0),0.0)

#
# Functions
#

def IPA_edge(img, op_type):
  """ 
    Edge detection (not localization)
    (op_type=roberts,prewitt,sobel) 
  """
  if op_type=='roberts':
    return IPA_edge_roberts(img)
  elif op_type=='prewitt':
    return IPA_edge_prewitt(img)
  elif op_type=='sobel':
    return IPA_edge_sobel(img)
  return None

def IPA_edge_roberts(img):
  """ Roberts edge detector """
  m1=np.array([[1,0],[0,-1]])
  m2=np.array([[0,-1],[1,0]])
  im1=morpho.IPA_conv2(img,m1,op=conv_op_unbound,pad_type=2)
  im2=morpho.IPA_conv2(img,m2,op=conv_op_unbound,pad_type=2)
  return morpho.IPA_apply(sum_op_abs,im1,im2)

def IPA_edge_prewitt(img):
  """ Prewitt edge detector """
  m1=np.transpose(np.array([ [1,1,1] ]))
  m2=np.array([[1,0,-1]])
  im1=morpho.IPA_conv2(morpho.IPA_conv2(img, m1, op=conv_op_unbound, pad_type=2), m2, op=conv_op_unbound, pad_type=2)
  m1=np.transpose(np.array([[1,0,-1]]))
  m2=np.array([[1,1,1]])
  im2=morpho.IPA_conv2(morpho.IPA_conv2(img, m1, op=conv_op_unbound, pad_type=2), m2, op=conv_op_unbound, pad_type=2)
  return morpho.IPA_apply(sum_op_abs, im1, im2)

def IPA_edge_sobel(img):
  """ Sobel edge detector """
  m1=np.transpose(np.array([[1,2,1]]))
  m2=np.array([[1,0,-1]])
  im1=morpho.IPA_conv2(morpho.IPA_conv2(img, m1, op=conv_op_unbound,pad_type=2), m2, op=conv_op_unbound, pad_type=2)
  m1=np.transpose(np.array([[1,0,-1]]))
  m2=np.array([[1,2,1]])
  im2=morpho.IPA_conv2(morpho.IPA_conv2(img, m1, op=conv_op_unbound, pad_type=2),  m2, op=conv_op_unbound, pad_type=2)
  return morpho.IPA_apply(sum_op_abs, im1, im2)

def  IPA_meanfilter(img,mask_size):
  """ 
    Performs mean filtering (mask_size is a vector containing X,Y size, eg. [3 3]) 
    (Unoptimized - method b)
  """
  x,y=mask_size
  m1=np.array([[1.0/(x*y) for i in range(x) ]])
  m2=np.array([[1.0/(x*y)] for j in range(y)])
  return morpho.IPA_conv2(morpho.IPA_conv2(img, m1, op=conv_op, pad_type=2), m2, op=conv_op, pad_type=2)

def  IPA_Gfilter(img, mask_size, sigma):
  """ 
    Performs Gaussian filtering using sigma 
    (Unoptimized - no 1D gauss separation)
  """
  c=1/(2.0*sigma)
  a=c*1.0/np.pi
  gauss=lambda u,v: a*np.exp(-(pow(u,2.0)+pow(v,2.0))/c) 
  filt=np.zeros((mask_size[0],mask_size[1]))
  for i in range(mask_size[0]):
    for j in range(mask_size[1]):
      filt.itemset((i,j),gauss((i-mask_size[0]/2), (j-mask_size[1]/2)))
  return morpho.IPA_conv2(img, filt, op=conv_op, pad_type=2)

