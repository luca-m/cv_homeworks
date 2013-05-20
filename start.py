#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Luca Mella"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2013/05/20 $"
__copyright__ = "Copyright (c) 2012-2013 Luca Mella"
__license__ = "CC BY-NC-SA"

import argparse
import inspector_helper as insp
import traceback
import string

def main():
	hmworks=[string.split(s,'.')[1] for s in insp.list_modules('hworks') ]
	parser=argparse.ArgumentParser("")
	parser.add_argument('homework',choices=hmworks)
	parser.add_argument('input')
	#parser.add_argument('output')
	args=parser.parse_args()

	try:
		h=insp.import_package('hworks.'+args.homework)
		h=insp.get_modules(h)[args.homework]
		h.run(args.input,None)
	except Exception, e:
		print "EXCEPTION:\n%s"%str(e)
		print "%s"%traceback.format_exc()

if __name__ == "__main__":
	main()

