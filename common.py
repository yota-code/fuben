#! /usr/bin/env python

import re

__re_format = re.compile(r"(^%\d?d$)|(^%\d?\.?\d?f$)")
__re_float_format = re.compile(r"^%\d?\.?\d?f$")

boolean_ = { True : "%__true__%", False : "%__false__%" }
# return boolean_.get(b, "")


def read_int(s, default = None) :
	try :
		return int(s)
	except :
		return default
	
def read_float(s, default = None) :
	try :
		return float(s)
	except :
		return default

def read_fmt(f_args, default_fmt="%s") :
	arg_0 = f_args[0][0]
	if re.search(__re_format, arg_0) :
		return "%" + arg_0, f_args[1:]
	else :
		return default_fmt, f_args
