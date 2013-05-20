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

	print "IPA_histo"
	hist=IPA_histo(im,ranges)
	print "IPA_histoConvolution1D Moving Average"
	hist_avg=IPA_histoConvolution1D(hist,[1/11.0]*11)
	print "IPA_histoConvolution1D Gaussian"
	hist_gauss=IPA_histoConvolution1D(hist,[1,2,3,4,5,4,3,2,1])
	print "IPA_histoNorm"
	hist_norm=IPA_histoNorm(hist,im.size)
	print "IPA_histoCdf"
	hist_cdf=IPA_histoCdf(hist_norm)
	print "IPA_histoTransform"
	im_eq=IPA_histoTransform(im,hist_cdf)
	print "IPA_FindThreshold_Isodata"
	thr_isodata=IPA_FindThreshold_Isodata(hist_avg)
	print "IPA_Bynarize"
	im_thr_isodata=IPA_Bynarize(im,thr_isodata)
	print "IPA_FindThreshold_Otsu"
	thr_otsu=IPA_FindThreshold_Otsu(hist_avg)
	print "IPA_Bynarize"
	im_thr_otsu=IPA_Bynarize(im,thr_otsu)
	print "IPA_histoTransform"
	[p,v]=IPA_PeakValley(hist_gauss)

	print "Plotting.."
	plots.plotHist(hist_avg,"Averaged Histogram (moving average filter)")
	plots.plotHistPeakValley(hist_gauss,p,v,"Peaks and valley")
	plots.plotHist(hist_norm,"Normalized histogram")
	plots.plotHist(hist_avg,"Histogram (+Isodata)",thr_isodata)
	plots.plotHist(hist_avg,"Histogram (+Otsu)",thr_otsu)
	plots.plotHist(hist_cdf,"Cumulative histogram")
	plots.plotImage(im,"Original Image")
	plots.plotImage(im_eq,"Equalized Image")	
	plots.plotImage(im_thr_isodata,"Binarizer (Isodatata)")
	plots.plotImage(im_thr_otsu,"Binarizer (Otsu)")
	
	plots.showPlots()

# Histogram Functions
def IPA_histo(im, rang=[0,255]):
	""" Calculate an histogram """
	hist=np.array( [0]*(rang[1]-rang[0]) )
	for p in np.nditer(im):
		hist[p]=hist[p]+1
	return hist
def IPA_histoNorm(hist,nvals=None):
	""" Normalize an histogram """
	if not type(hist) == np.array:
		hist=np.array(hist)
	if nvals is None:
		m=float(sum(hist))
	else:
		m=float(nvals)
	return hist/m
def IPA_histoConvolution1D(hist, mask):
	""" 0-padded 1D convolution """
	mx = len(mask)
	ix = len(hist)
	mcx=mx/2
	nhist=np.array([0]*ix)
	for j in range(ix):
		val=0
		for q in range(mx):
			if j+q-mcx<0 or j+q-mcx>=ix:
				tmp=0 # 0-padding
			else:
				tmp= hist[j+q-mcx]*mask[q]
			val+=tmp
		nhist[j]=val 
	return nhist
def IPA_histoCdf(hist,nvals=None):
	""" histogram CDF """
	return np.array(np.cumsum(hist))
def IPA_histoTransform(im,new_histo):
	""" Histogram transformation function """
	nim=im.copy()
	x,y=nim.shape
	for i in range(x):
		for j in range(y):
			tmp=nim.item(i,j)
			nim.itemset((i,j),new_histo[tmp]*len(new_histo))
	return nim
def IPA_Bynarize(im,threshold):
	""" Bynarize a Greyscale image """
	nim=im.copy()
	x,y=nim.shape
	for i in range(x):
		for j in range(y):
			tmp=0
			if nim.item(i,j)>threshold:
				tmp=1
			nim.itemset((i,j),tmp)
	return nim
def IPA_FindThreshold(hist,type):
	""" Histogram transformation function """
	if type=='otsu':
		return IPA_FindThreshold_Otsu(hist)
	elif type=='isodata':
		return IPA_FindThreshold_Isodata(hist)
def IPA_FindThreshold_Otsu(hist):
	""" Otsu thresholding (Unoptimized) """
	if not type(hist) == np.array:
		hist=np.array(hist)
	m_sig=float("-inf")
	t_max=-1
	tot=sum(hist)
	sall=sum(np.multiply(range(len(hist)),hist))
	wb=0
	sb=0
	mb=0
	wf=0
	mf=0
	for t in range(len(hist)):
		wb+=hist[t] # cumulative sum
		if wb==0:
			continue
		wf=tot-wb
		if wf==0:
			break
		sb+=t*hist[t]
		mb=sb/wb
		mf=(sall-sb)/wf
		sig= wb*wf*(mb-mf)**2 # in-between
		# in-between sigma square (unoptimized)
		# sig=np.sum( np.multiply(range(t),hist[:t]) ) * \
		#	np.sum( np.multiply(range(t,len(hist)),hist[t:]) )* \
		#	np.power( np.sum(np.multiply(range(t),hist[:t]))/np.sum(hist[:t]) - \
		#		      np.sum(np.multiply(range(t,len(hist)),hist[t:]))/np.sum(hist[t:]),2)
		if sig>m_sig:
			m_sig=sig
			t_max=t
	return t_max
def IPA_FindThreshold_Isodata(hist):
	""" Isodata thresholding (Unoptimized) """ 
	if not type(hist) == np.array:
		hist=np.array(hist)
	thr=-1
	thr_new=127
	while thr!=thr_new:
		thr=thr_new
		mb=np.sum( np.multiply(range(thr),hist[:thr]) ) / sum(hist[:thr])
		mf=np.sum( np.multiply(range(thr,len(hist)),hist[thr:]) ) / sum(hist[thr:])
		thr_new=(mb+mf)/2
	return thr_new
def IPA_PeakValley(hist):
	""" Peak and Valley with derivate and dumb zero-crossing"""
	if not type(hist) == np.array:
		hist=np.array(hist)
	hist_d1=IPA_histoConvolution1D(hist,[-1.0,1.0]) # first derivate of the histo
	valley=[]
	peaks=[]
	for i in range(len(hist_d1)-1):
		if hist_d1[i]>0 and hist_d1[i+1]<=0:
			peaks+=[i]
		elif hist_d1[i]<=0 and hist_d1[i+1]>0:
			valley+=[i]
	return [peaks,valley]