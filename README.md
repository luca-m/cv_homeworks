CV Homeworks
============

Elab.Immagini LM 2012/2013

luca.mella@studio.unibo.it

#### Primitives demo (python)

Homework 1,2 and 3 have been developed in Python, usage:

```
python homework.py -h              

usage: [-h] {filter,histo,morpho} input

positional arguments:
  {filter,histo,morpho}
  input input image

optional arguments:
  -h, --help            show this help message and exit
```   

_DISCLAIMER: Convolution in Python is pretty __SLOW__.. 
This does not mean that python cannot be used 
for this kind of computation but also mean that we should use libraries like 'numpy' or 'cv' which provide
access to native algorithm implementation (read 'C/C++') directly from python.
However, this is only a homework.._
      
      
#### Cell segmentation (matlab/linux)
    
Homework 4 has been developed in `Matlab`, launching it via linux shell: 

```  
matlab -nodesktop -nosplash < <(echo "cellseg('tumor_microscopy_c.tif')";read)
```


