# -*- coding: utf-8 -*-

__author__ = "Luca Mella"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2013/05/20 $"
__copyright__ = "Copyright (c) 2012-2013 Luca Mella"
__license__ = "CC BY-NC-SA"

""" 
MATHEMATICAL MORPHOLOGY
  All the routines must work with logical (B/W) and greyscale images, with
  automatic detection of image type.
  Alternatively, you can build different functions for greyscale and binary images.

  IPA_im2bw(img,th)
  IPA_morph(img,mask,op_type)
  IPA_closing(img,mask)
  IPA_opening(img,mask)
  IPA_hitmiss(img,SE1,SE2)
  IPA_tophat(img,mask)
  IPA_bothat(img,mask)
  IPA_top-bot_enhance(img,mask)
  IPA_imreconstruct(marker,mask,SE1)

NOTE: input image is loaded in grayscale and thresholded at with OTSU method (after a gaussian smoothing).

"""

import cv2
import numpy as np
import histo         # NOTE: rely on thresholding function implemented in hworks.histo
import plots

def run(inImPath,outImPath):
  print "DISCLAIMER: Convolution in Python is pretty SLOW.."
  print "            This does not mean that python cannot be used for this kind of computation,"
  print "            but also mean that we should use libraries like 'numpy' or 'cv' which provide"
  print "            access to native algorithm implementation (read 'C/C++') directly from python."
  print "            However, this is only a homework.."
  im=cv2.imread(inImPath, cv2.CV_LOAD_IMAGE_GRAYSCALE)
  square_3x3=IPA_se_square(3)
  
  print "[MORPHO] IPA_im2bw"
  gauss_kernel=[1,2,3,4,5,4,3,2,1] 
  gauss_kernel_norm= [float(x)/sum(gauss_kernel) for x in gauss_kernel]
  im_bin=IPA_im2bw(im,histo.IPA_FindThreshold_Otsu(histo.IPA_histoConvolution1D(histo.IPA_histo(im, rang=[0,255]),gauss_kernel_norm)))
  #im_bin=IPA_im2bw(im,1)
  # Binary ops
  print "[MORPHO] IPA_dilate"
  im_bin_dil=IPA_dilate(im_bin,square_3x3)
  print "[MORPHO] IPA_erode"
  im_bin_ero=IPA_erode(im_bin,square_3x3)
  print "[MORPHO] IPA_opening"
  im_bin_open=IPA_opening(im_bin,square_3x3)
  print "[MORPHO] IPA_closing"
  im_bin_close=IPA_closing(im_bin,square_3x3)
  print "[MORPHO] IPA_imreconstruct"
  im_bin_ric=IPA_imreconstruct(im_bin_open,im_bin,square_3x3)
  # Gray scale ops
  print "[MORPHO] IPA_dilate"
  im_dil=IPA_dilate(im,square_3x3)
  print "[MORPHO] IPA_erode"
  im_ero=IPA_erode(im,square_3x3)
  print "[MORPHO] IPA_opening"
  im_open=IPA_opening(im,square_3x3)
  print "[MORPHO] IPA_closing"
  im_close=IPA_closing(im,square_3x3)
  print "[MORPHO] IPA_imreconstruct"
  im_ric=IPA_imreconstruct(im_open,im,square_3x3)
  print "[MORPHO] IPA_tophat"
  im_tophat=IPA_tophat(im,square_3x3)
  print "[MORPHO] IPA_bothat"
  im_bothat=IPA_bothat(im,square_3x3)
  print "[MORPHO] IPA_topbot_enhance"
  im_topbot=IPA_topbot_enhance(im,square_3x3)
  
  print "Plotting.."
  plots.plotImage(im_bin,"[MORPHO] Bin Original")
  plots.plotImage(im_bin_ero,"[MORPHO]Bin Eroded")
  plots.plotImage(im_bin_dil,"[MORPHO]Bin Dilated")
  plots.plotImage(im_bin_open,"[MORPHO]Bin Opening")
  plots.plotImage(im_bin_close,"[MORPHO]Bin Closing")
  plots.plotImage(im_bin_ric,"[MORPHO]Bin Reconstruction (geodesic dilation)")
  plots.plotImage(im,"[MORPHO] Gray Original")
  plots.plotImage(im_ero,"[MORPHO] Gray Eroded")
  plots.plotImage(im_dil,"[MORPHO] Gray Dilated")
  plots.plotImage(im_open,"[MORPHO] Gray Opening")
  plots.plotImage(im_close,"[MORPHO] Gray Closing")
  plots.plotImage(im_ric,"[MORPHO] Gray Reconstruction (geodesic dilation)")
  plots.plotImage(im_tophat,"[MORPHO] Gray TopHat")
  plots.plotImage(im_bothat,"[MORPHO] Gray BotHat")
  plots.plotImage(im_topbot,"[MORPHO] Gray TopBot Enanche")
  plots.showPlots()

def IPA_se_square(size):
  """ Squared structural element """
  return np.matrix([[1]*size for i in range(size)])

def IPA_apply(fun, *imgs):
  """ 
    Obtain a new image by appling the specified 
    function on every couple of pixels
  """
  shp=imgs[0].shape
  for x in imgs:
    if x.shape!=shp:
      raise Exception("Images must have the same shape")
  y,x=shp
  nim=np.zeros((y,x))
  for j in range(y):
    for i in range(x):
      params=[p.item(j,i) for p in imgs]  # Pick the j,i pixel of each image in imgs
      nim.itemset((j,i),fun(*params))     # pass these pixels to the function and put the 
                                          # result in the j,i pixel of the new image
  return nim    # Otherwise np.array(map(fun, imgs))

def IPA_conv2(img, mask, op=lambda px, mask, val:0.0 ,pad_type=1, init=lambda px:0):
  """ 
    Performs a convolution-like user defined local operation.
    
    Supported padding:
      zero-padding  (pad_type=1)
      replicate     (pad_type=2)
    
    The user defined operation MUST return a float value and 
    MUST handle 3 input parameters: 
        
        pixel, mask, prev_value

    Also user may specify an initialization function that could
    be useful to specify in case of erosion operation. 
    In this case the function must return a float and handle 1 param.

  """ 
  my,mx = mask.shape
  iy,ix = img.shape
  if iy/my<=0 or ix/mx<=0:
    raise Exception("Mask must be smaller than image")
  mcx=mx/2
  mcy=my/2
  nim=np.zeros((iy,ix))
  for i in range(iy):
    for j in range(ix):
      val=init(img.item(i,j))
      for p in range(my):
        for q in range(mx):
          if i+p-mcy<0 or j+q-mcx<0 or i+p-mcy>=iy or j+q-mcx>=ix:
            if pad_type==1:       # 0-padding
              impix=0
            elif pad_type==2:     # repricate-padding
              ip,iq=(0,0)
              if i+p-mcy<0:
                ip=i+p+mcy 
              if j+q-mcx<0:
                iq=j+q+mcx
              if i+p-mcy>=iy:
                ip=i+p-my
              if j+q-mcx>=ix:
                iq=j+q-mx
              impix=img.item(ip,iq)
          else:
            impix=img.item(i+p-mcy, j+q-mcx)
          val=op(impix, mask.item(p,q), val)
      nim.itemset((i,j),val) 
  return nim

def IPA_im2bw(img,th):
  """ Binarize """
  return histo.IPA_Bynarize(img,th)

def IPA_morph(img,mask,op_type):
  """ 
    Morphological primitives 
    op_type=(dilate,erode) 
  """
  if op_type=='dilate':
    return IPA_dilate(img,mask)
  elif op_type=='erode':
    return IPA_erode(img,mask)
  return None

def IPA_dilate(img,mask):
  """ Morphological Dilatation """
  return IPA_conv2(img, mask, op=lambda px,msk,val:max(msk*px,val), pad_type=2)

def IPA_erode(img,mask):
  """ Morphological Erosion """
  return IPA_conv2(img, mask, op=lambda px,msk,val:min(msk*px,val), pad_type=2,init=lambda px:px)

def IPA_closing(img,mask):
  """ Closing """
  return IPA_erode(IPA_dilate(img,mask),mask)

def IPA_opening(img,mask):
  """ Opening """
  return IPA_dilate(IPA_erode(img,mask),mask)

def IPA_hitmiss(img,SE1,SE2,fun=min):
  """ Binary hit and miss """
  return IPA_apply(fun, IPA_erode(img,SE1), IPA_erode(IPA_apply(lambda a:1^int(a), img), SE2))

def IPA_tophat(img,mask):
  """ Top Hat """
  return IPA_apply(lambda a,b:max(a-b,0), img, IPA_opening(img, mask))

def IPA_bothat(img,mask):
  """ Bottom Hat """
  return IPA_apply(lambda a,b:max(a-b,0), IPA_closing(img, mask), img)

def IPA_topbot_enhance(img,mask):
  """ TopHat BottomHat enanchment """
  #  - (+ img tophat) bothat
  return IPA_apply(lambda a,b:max(a-b,0),     
                          IPA_apply(lambda a,b:min(a+b,255), img, IPA_tophat(img,mask)), 
                          IPA_bothat(img,mask))

def IPA_imreconstruct(marker, mask, SE, method='dilate', niter=4):
  """ Reconstruction by geodesic dilation/erosion (dilate/erode) """
  stop=False
  new_marker=None
  i=0
  while not stop and i<niter:
    new_marker=IPA_apply(min, IPA_morph(marker, SE, method), mask)
    i+=1
    if (new_marker!=marker).any():
      marker=new_marker;
    else:
      stop=True
  return new_marker

