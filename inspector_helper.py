#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Luca Mella"
__version__ = "$Revision: 0.4 $"
__date__ = "$Date: 2013/05/20 $"
__copyright__ = "Copyright (c) 2012-2013 Luca Mella"
__license__ = "CC BY-NC-SA"

import os
import inspect

# Some global vars
default_arg_filter = lambda s : s not in ['self']
default_object_filter = lambda s : not s.startswith('_')
default_module_filter = lambda s : not s.startswith('_') and s.endswith('.py')

# Code inspection utility function

def list_modules(path='.', recoursive=False , filtr=default_module_filter ):
	"""
	List all modules files according to specified parameters (path, subdirs and name filter)
	"""
	mods=list()
	for dirname, dirnames, filenames in os.walk(path):
		for f in filenames :
			if filtr(f):
				mods.append((dirname.replace("/",".")+".").replace("..","")+f.replace(".py",""))
		if not recoursive :
			return mods
	return mods

def import_package(package='.'):
	"""
	Import a module (dynamically)
	"""
	mod = __import__(package) #, fromlist=[])
	return mod

def get_members(module_or_clazz_or_object):
	"""
	Obtain a dictionary representing the specified entity
	"""
	if type(module_or_clazz_or_object).__name__=='dict':
		return module_or_clazz_or_object
	else:
		fun=dict()
		for k,v in inspect.getmembers(module_or_clazz_or_object):
			fun[str(k)]=v
		return fun
	
def get_modules(module, filtr=default_object_filter ):
	"""
	Obtain all the modules contained by the specified module
	"""
	fun=dict()
	for (k,v) in get_members(module).items():
		if filtr(k) and inspect.ismodule(v):
			fun[str(k)]=v
	return fun
		

def get_functions(module, filtr=default_object_filter ):
	"""
	Obtain all the functions defined in the specified module
	"""
	fun=dict()
	for (k,v) in get_members(module).items():
		if filtr(k) and inspect.isfunction(v):
			fun[str(k)]=v
	return fun

def get_arguments(func_or_method, filtr=default_arg_filter ):
	"""
	Obtain all the functionsparameter specified in the method
	"""
	return [x for x in func_or_method.func_code.co_varnames if filtr(x)]

def get_classes(module_or_clazz_or_object_or_dict, filtr=default_object_filter):
	"""
	Obtain all the classes defined in the specified module
	"""
	fun=dict()
	for (k,v) in get_members(module_or_clazz_or_object_or_dict).items():
		if filtr(k) and inspect.isclass(v):
			fun[str(k)]=v
	return fun

def get_methods(clazz_or_object_or_dict, filtr=default_object_filter ):
	"""
	Obtain all the methods defined in the specified class or object
	"""
	fun=dict()
	for (k,v) in get_members(clazz_or_object_or_dict).items():
		if filtr(k) and inspect.ismethod(v) :
			fun[str(k)]=v
	return fun

def get_classmethods(clazz_or_object_or_dict, filtr=default_object_filter):
	"""
	Obtain all classmethods defined in the specified class.
	ClassMethods are quite similar to Java static class methods,
	but they can be specialized using subclassing mechanism.
	Differs from "object methods" because its implicit parameter
	is the python Class itself (not the instace ie. self)
	"""
	fun=dict()
	for (k,v) in get_members(clazz_or_object_or_dict).items():
		if filtr(k) and inspect.isfunction(v):
			fun[str(k)]=classmethod(v)
	return fun

def get_staticmethods(clazz_or_object_or_dict, filtr=default_object_filter):
	"""
	Obtain all static methodes defined in the specified class.
	Staticmethod have much more similar to Java static class methods.
	No implicit parameter is passed. Close to a module function.
	"""
	fun=dict()
	for (k,v) in get_members(clazz_or_object_or_dict).items():
		if filtr(k) and inspect.isfunction(v):
			fun[str(k)]=staticmethod(v)
	return fun

# option parsing

