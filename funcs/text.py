#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" Set of text functions for the PrettyTag printer
"""

import sys, re
from common import *

def text_lpadd(f_args) :
	"""	return a string of length arg3 where arg1 is aligned on the left. The
	remaining space is padded with arg2
	
	ex:	&lpadd(sentence,ABcdefg,18)       -> sentenceABcdefgABc
		&lpadd(other sentence,ABcdefg,18) -> other sentenceABcd
	"""
	l = read_int(f_args[2][0])
	m = f_args[1][0] * (((l - len(f_args[0][0]) - 1) / len(f_args[1][0])) + 1) 
	return (f_args[0][0] + m)[0:l]
	
def text_lfill(f_args) :
	"""	return a string of length arg3 filled with arg2 where arg1 is left aligned
	
	ex:	&lfill(sentence,ABcdefg,18)       -> sentenceBcdefgABcd
		&lfill(other sentence,ABcdefg,18) -> other sentenceABcd
	"""
	l_0 = len(f_args[0][0])
	l_1 = len(f_args[1][0])
	n_0 = read_int(f_args[2][0])
	m = (f_args[1][0] * (((n_0 - 1) / l_1) + 1))[0:n_0]
	return f_args[0][0][0:l_0] + m[l_0:]
	
def text_upper(f_args) :
	try :
		return f_args[0][0].upper()
	except :
		return ""
	
def text_lower(f_args) :
	try :
		return f_args[0][0].lower()
	except :
		return ""
	
	
def text_capitalize(f_args) :
	m = "all"
	if len(f_args) == 2:
		m = f_args[1][0].strip()
	if m not in ["first", "all", "smart_en"]:
		return "#ERROR#:text_capitalize:unknown mode \"%s\"" % (m,)
	if m == "first" :
		return f_args[0][0].capitalize()
	elif m == "smart_en" :
		_capitalize_list = []
		for s in f_args[0][0].capitalize().split(" ") :
			if s not in ["a", "of", "to", "up", "down", "for", "with", "and", "or"] :
				s = s.capitalize()
			_capitalize_list.append(s)
		return " ".join(_capitalize_list)
	else :
		return " ".join([s.capitalize() for s in f_args[0][0].split(" ")])
	
def text_substring(f_args) :
	try :
		if len(f_args) != 3:
			return """#ERROR#:substring:takes exactly 3 arguments, %d given##""" % (len(f_args))
		f = read_int(f_args[0][0])
		l = read_int(f_args[1][0])
		return f_args[2][0][f:l]
	except :
		return ""
		
register = {
	"lpadd" : text_lpadd,
	"lfill" : text_lfill,
	"upper" : text_upper,
	"lower" : text_lower,
	"capitalize" : text_capitalize,
	"substring" : text_substring,
}
