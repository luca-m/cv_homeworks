# -*- coding: utf-8 -*-

__author__ = "Luca Mella"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2013/05/20 $"
__copyright__ = "Copyright (c) 2012-2013 Luca Mella"
__license__ = "CC BY-NC-SA"

import matplotlib.pyplot as plt

FIG=0

def plotHist (hist,title="",thrshld=None):
	""" """
	global FIG
	plt.figure(FIG)
	for i in range(0, len(hist)):
		plt.vlines(i, 0, hist[i])
	if thrshld is not None:
		plt.vlines(thrshld,-max(hist)/2,0)
	plt.title(title)
	FIG+=1
def plotHistPeakValley (hist,peaks,valley,title=""):
	""" """
	global FIG
	plt.figure(FIG)
	m=max(hist)
	for i in range(0, len(hist)):
		plt.vlines(i, 0, hist[i])
	for i in peaks:
		plt.vlines(i, m, m+1009)
	for i in valley:
		plt.vlines(i, -100, -1100)
	plt.title(title)
	FIG+=1
def plotImage(im,title=""):
	""" """
	global FIG
	plt.figure(FIG)
	plt.imshow(im)
	plt.set_cmap('gray')
	plt.title(title)
	FIG+=1
def showPlots():
	""" """
	plt.show()