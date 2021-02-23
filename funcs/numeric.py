#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" numerical functions for the PrettyTag printer
"""

import sys, re
from fuben_disabled.common import *

def numeric_add(f_args) :
	"""	add = arg1 + arg2 + ... + argn
	"""
	_fmt, f_args = extract_fmt(f_args, "%s")
	_out = 0.0
	for arg in f_args :
		_out += read_float(arg[0], 0.0)
	return _fmt % (_out,)
	
def numeric_inv(f_args) :
	"""	inv = (1 / arg1) + (1 / arg2) + ... + (1 / argn)
	"""
	_fmt, f_args = extract_fmt(f_args, "%s")
	_out = 0.0
	for arg in f_args :
		val = read_float(arg[0], 1.0)
		if val == 0.0 :
			return "#ERROR#:numeric_inv:can not divide by zero"
		_out += (1.0 / val)
	return _fmt % (_out,)
	
def numeric_mod(f_args) :
	"""	mod = True if arg1 % arg2 == 0 else False
	"""
	val = read_int(f_args[1][0])
	if val == 0.0 :
		return "#ERROR#:numeric_isModulo:can not take 0 as second argument"
	_out = (read_int(f_args[0][0]) % val)
	return _fmt % (_out,)
	
def numeric_isModulo(f_args) :
	"""	return True if arg1 % arg2 == 0 else False
	"""
	val = read_int(f_args[1][0])
	if val == 0.0 :
		return "#ERROR#:numeric_isModulo:can not take 0 as second argument"
	_is = ((read_int(f_args[0][0]) % val) == 0)
	return boolean_.get(_is, "")
	
def numeric_isEqual(f_args) :
	"""	return True if arg1 % arg2 == 0 else False
	"""
	a = read_float(f_args[0][0],0.0)
	b = read_float(f_args[1][0],0.0)
	_is = (a == b)
	return boolean_.get(_is, "")
	
def numeric_mul(f_args) :
	"""	return arg1 * arg2 * ... * argn
	"""
	_fmt, f_args = extract_fmt(f_args, "%s")
	_out = 1.0
	for arg in f_args :
		_out *= read_float(arg[0], 1.0)
	return _fmt % (_out,)
	
#def __numeric_neg(f_args) :
#	"""	
#	&numeric_neg( i1 , i2 , ... , in )
#		return - i1 - i2 - ... - in
#	"""
#	_fmt, f_args = extract_fmt(f_args, "%s")
#	_out = 0.0
#	for arg in f_args :
#		_out -= read_float(arg[0], 1.0)
#	return _fmt % (_out,)
	
#def __numeric_sub(f_args) :
#	_fmt, f_args = extract_fmt(f_args, "%s")
#	_out = read_float(f_args.pop(0)[0], 0.0)
#	for arg in f_args :
#		_out -= read_float(arg[0], 1.0)
#	return _fmt % (_out,)

#def __numeric_div(f_args) :
#	_fmt, f_args = extract_fmt(f_args, "%s")
#	_out = read_float(f_args.pop(0)[0], 1.0)
#	for arg in f_args :
#		a = read_float(arg[0], 1.0)
#		if a == 0.0 :
#			return "#ERROR#:numeric_div:can not divide by zero"
#		_out *= ( 1.0 / a )
#	return _fmt % (_out,)

#def apply_seq_operator(f_args, operator, default_val, init_val= None, default_fmt="%d") :
#	_fmt, f_args = extract_fmt(f_args, default_fmt)
#	_out = init_val if init_val != None else default_val
#	for arg in f_args :
#		_out = operator(_out, read_float(arg[0], default_val))
#	return _fmt % (_out,)
#	
#def apply_bin_operator(f_args, operator, default_val, default_fmt="%d") :
#	_fmt, f_args = extract_fmt(f_args, default_fmt)
#	a = read_float(f_args.pop(0)[0], default_val)
#	b = read_float(f_args.pop(0)[0], default_val)
#	_out = operator(a,b)
#	return _fmt % (_out,)
	
#def numeric_truediv(f_args) :
#	return apply_bin_operator(f_args, operator.truediv, 1.0, "%s")
#
#def __isModulo(f_args) :
#	m = read_int(f_args[1][0])
#	if m == 0 :
#		return "#ERROR#:numeric_isModulo:can not take 0 as second argument"
#	_is = ((read_int(f_args[0][0]) % m) == 0)
#	return boolean_.get(_is, "")
#	
#def __inv(f_args) :
#	_fmt, f_args = extract_fmt(f_args, "%0.3f")
#	_out = 1.0
#	for arg in f_args :
#		_out *= (1.0 / read_float(arg[0], 1.0))
#	return _fmt % (_out,)
#	
#def __add(f_args) :
#	_fmt, f_args = extract_fmt(f_args, "%d")
#	_out = 0.0
#	for arg in f_args :
#		_out += read_float(arg[0], 0.0)
#	return _fmt % (_out,)
#	
#def __remainder(f_args) :
#	m = read_int(func_arg_list[1][0])
#	if m == 0 :
#		return "#ERROR#:numeric_remainder:can not take 0 as second argument"
#	return "%d" %(read_int(func_arg_list[0][0]) % m,)

	
if __name__ == '__main__' :
	tests = [
		[numeric_add, ["1.2","2.0"], ""],
		[numeric_mul, ["1.2","2.0"], ""],
		[numeric_isEqual, ["1.2","2.0"], ""],
		[numeric_isEqual, ["1.2","1.2"], ""],
		[numeric_isEqual, ["2.0","2"], ""],
	]
		
	for u in tests :
		f_args = [(i, True) for i in u[1]]
		print(u, u[0](f_args))
