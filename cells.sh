#!/bin/bash
## cells.sh
##
## Copyright (C) 2014 stk <stk@101337>
## Distributed under terms of the MIT license.
##
## Description:
##
##    Cell segmentation assignment
##
## Usage:
##
##    cells OPTIONS PARAMS
##
## Parameters:
##    
##    NA
##
## Options:
##    
##    -h, --help    This help message
##
## Example:
##    
##    cells -h
##

# ----------------
# UTILITY FUNCTIONS
# ----------------

echoerr() { 
  echo "$@" 1>&2; 
}
usage() {
  [ "$*" ] && echoerr "$0: $*"
  sed -n '/^##/,/^$/s/^## \{0,1\}//p' "$0" 1>&2
  exit 2
}

# ----------------
# FUNCTIONS
# ----------------


# ----------------
# MAIN
# ----------------

# Options parsing
while [ $# -gt 0 ]; do
  case $1 in
    (-h|--help) usage 2>&1;;
    (--) shift; break;;
    (-*) usage "$1: unknown option";;
    (*) break;;
  esac
done

cd matlab
matlab -nodesktop -nosplash < <(echo "cellseg('tumor_microscopy_c.tif')";read)




