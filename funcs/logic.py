#! /usr/bin/env python

""" logical functions for the PrettyTag formatter

In the following prototypes, a 'condition' can be:
 - the return value of another logical function
 - %__true__% or %__false__%, two special tags which are respectively
	always True and False
 - a tag picking attempt (True if the tag is found else False)
"""

import sys, re
#from fuben.common import *

def logic_if(f_args) :
	"""&if(condition, arg_1 , arg_2)
	
	if condition : 
		return arg_1
	else :
		return arg_2
	"""
	if len(f_args) != 3 :
		return """#ERROR#:if:takes exactly 3 arguments, %d given##""" % (len(f_args))
	if f_args[0][1] == True :
		return f_args[1][0]
	else :
		return f_args[2][0]

def logic_or(f_args) :
	"""&or(condition_1, condition_2, ..., condition_n)
	
	return condition_1 or condition_2 or ... or condition_n"""
	_is = False
	for arg in f_args :
		_is = _is or arg[1]
	return boolean_.get(_is, "")
	
def logic_and(f_args) :
	"""&and(condition_1, condition_2, ..., condition_n)
	
	return condition_1 and condition_2 and ... and condition_n"""
	_is = True
	for arg in f_args :
		_is = _is and arg[1]
	return boolean_.get(_is, "")
	
def logic_not(f_args) :
	"""&not(condition_1, condition_2, ..., condition_n)
	
	return not ( condition_1 xor condition_2 xor ... xor condition_n)"""
	return logic_xor(f_args, inversed_logic=True)
	
def logic_xor(f_args, inversed_logic=False) :
	"""&xor(condition_1, condition_2, ..., condition_n)
	
	return condition_1 xor condition_2 xor ... xor condition_n"""
	_is = inversed_logic
	for arg in func_arg_list :
		_is = (_is and (not arg[1])) or ((not _is) and arg[1])
	return boolean_.get(_is, "")
	
	
register = {
	"if" : logic_if,
	"or" : logic_or,
	"and" : logic_and,
	"not" : logic_not,
	"xor" : logic_xor,
}
