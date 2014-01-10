#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Luca Mella"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2013/05/20 $"
__copyright__ = "Copyright (c) 2012-2013 Luca Mella"
__license__ = "CC BY-NC-SA"

import argparse
import traceback
import string

import hworks.histo
import hworks.histo_opencv
import hworks.filter
import hworks.morpho

def main():
  hwo=['histo','histo_opencv','filter','morpho']
  parser=argparse.ArgumentParser("Image processing homeworks.\nHere performance does not matter.\nDependencies: opencv2 python bindings, matplotlib.\n(Hit <CTRL+C> to exit)")
  parser.add_argument('homework',choices=hwo)
  parser.add_argument('input')
  args=parser.parse_args()
  try:
    if args.homework=='histo':
      hworks.histo.run(args.input,None)
    elif args.homework=='histo_opencv':
      hworks.histo_opencv.run(args.input,None)
    elif args.homework=='filter':
      hworks.filter.run(args.input,None)
    elif args.homework=='morpho':
      hworks.morpho.run(args.input,None)
  except Exception, e:
    print "EXCEPTION:\n%s"%str(e)
    print "%s"%traceback.format_exc()

if __name__ == "__main__":
  main()

