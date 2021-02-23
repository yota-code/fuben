#!/usr/bin/env python3.1

import sys, random, io, re
import timeit

#log.basicConfig(level=log.DEBUG)

__copyright__ = """
written and released under the terms of the most recent GPL
by C. Chassagne - 2009
"""

_PrettyTag__global_tag_ = {}
_PrettyTag__special_field_ = {
	"__true__" : ("%__true__%", True),
	"__false__" : ("%__false__%", False),
	"__tab__" : ("\t", True)
}

_PrettyTag__registered_functions = dict()

import funcs

load_list = ['logic']

class PrettyTag(object) :
	__mode_ = {
		"quote" : ('"', '"'),
		"tag" : ('%', '%'),
		"first" : ('[', '|'),
		"last" : ('[', ']'),
		"func_name" : ('&', '('),
		"func_args" : ('(', ')'),
		"func_arg" : ('', ','),
		"" : ('','')
	}
	
	def __init__(self) :
		self.__tag_ = {}
	
	def set_tag(self, tag_ , clear=False) :
		if clear : self.__tag_.clear()
		for i in tag_ :
			self.__tag_[i] = tag_[i]
			
	def updel_tag(self, key, value, format="%s") :
		if value != None :
			if type(value) != str :
				try :
					value = format % (value,)
				except :
					value = str(value)
			self.__tag_[key] = value
		else :
			self.__tag_.pop(key, None)
			
	def get_tag(self, name) :
		value = None
		if name in __special_field_ :
			value = __special_field_[name]
		if name in self.__tag_ :
			value = self.__tag_[name]
		if name in __global_tag_ :
			value = __global_tag_[name]
		if value != None :
			return value, True
		else :
			return "#NO_TAG_FOUND#", False
	
	def repr_boolean(self, b) :
		"""
			return a special value for booleans
		"""
		if b is True :
			return "%__true__%"
		elif b is False :
			return "%__false__%"
		else :
			return ""

	def call(self, f_name, f_args) :
		if f_name not in funcs.register :
			return "#ERROR#:call:&%s() not implemented" % (f_name,)
		return funcs.register[f_name](f_args)
		
	def __set_field(self, f_args) :
		self.__tag_[f_args[0][0]] = f_args[1][0]
		return ""
		
	def split(self, line_in, token) :
		pass
		
	def __set_multi(self, f_args) :
		n = 0
		tok = f_args.pop(0)[0].split(f_args.pop(0)[0])
		while n < len(tok) and 0 < len(f_args) :
			self.__tag_[f_args.pop(0)[0]] = tok[n]
			n += 1
		return ""
		
	def format(self, formatting_string, tag_ = None) :
		return self.parse(formatting_string, tag_=tag_)[1].getvalue()
		
	def sformat(self, stream, formatting_string, tag_ = None) :
		self.parse(formatting_string, line_out = stream, tag_=tag_)
		
	def parse(self, line_in, mode = "", depth = 0, line_out = None, tag_ = None) :
		if tag_ != None :
			self.set_tag(tag_, clear=True)
		if line_out == None :
			line_out = io.StringIO()
		
		end_token = self.__mode_[mode][1]
		
		isActive = True
		
		while(line_in != "") :
			c = line_in[0]
			line_in = line_in[1:]
			if c == '\\' :
				if mode in ["func_args", "last"] :
					line_out.write(c)
				line_out.write(line_in[0])
				line_in = line_in[1:]
				continue
			if c in end_token :
				return line_in, line_out, isActive
			if c == '"' :
				line_in, p, null = self.parse(line_in, "quote", depth + 1)
				line_out.write(p.getvalue())
				continue
			if c == '&' :
				if mode not in ["last"] :
					func_arg_list = []
					line_in, p, null = self.parse(line_in, "func_name", depth + 1)
					f_name = p.getvalue()
					line_in, p, null = self.parse(line_in, "func_args", depth + 1)
					f_args = p.getvalue() + (',')
					
					while f_args != '' :
						f_args, _arg, _isactive = self.parse(f_args, "func_arg", depth + 1)
						func_arg_list.append((_arg.getvalue(), _isactive))					
					p = self.call(f_name, func_arg_list)
					line_out.write(p)
					continue
			if c == '%' :
				if mode not in ["quote", "func_name", "func_args", "last"] :
					line_in, p, null = self.parse(line_in, "tag", depth + 1)
					tag_value, isActive = self.get_tag(p.getvalue())
					line_out.write(tag_value)
					continue
			if c == '[' :
				if mode not in ["quote", "func_name", "func_args"] :
					line_in, p, null = self.parse(line_in, "last", depth + 1)
					p.write("|")
					_in = p.getvalue()
					_isactive = False
					while _isactive == False :
						_in, p, _isactive = self.parse(_in, "first", depth + 1)
						_out = p.getvalue()
						if _isactive == True :
							isActive = True
							line_out.write(_out)
							break
						_out = ""
					continue
			
			line_out.write(c)

		return line_in, line_out, isActive


if __name__ == '__main__' : 
	u = [
		[r"[%truite%|coin]", "coin"],
		[r"&if(%title%,coin,)", "coin"],
#		[r"%__true__%", "%__true__%"],
#		[r"%__false__%", "%__false__%"],
#		[r"tabu%__tab__%lation", "tabu\tlation"],
#		[r"%title%", "TITLE"],
#		[r"[%titre%|no_title]", "no_title"],
#		[r"[%titre%|%title%|no_title]", "TITLE"],
#		[r"&and(%__true__%, %__true__%)","%__true__%"],
#		[r"&and(%__true__%, %__false__%)","%__false__%"],
#		[r"[%spam% artist ]ni", "ni"],
#		[r"[%artist% spam] ni", "ARTIST spam ni"],
#		[r"[%albumartist%|%artist% spam] ni", "ARTIST spam ni"],
#		[r"[%albumartist%|%artist% spam|%trackartist%] ni", "ARTIST spam ni"],
#		[r"&str_lower(SPAM %artist%)", "spam artist"],
#		[r"&str_capitalize(SPAM %artist%)", "Spam Artist"],
#		[r"&str_capitalize(lumberjack, spam)", "#ERROR#:str_capitalize:unknown mode \"spam\""],
#		[r"and now\, for \"something\" completely different", "and now, for \"something\" completely different"],
#		[r"&str_capitalize(and now\, for \"something\" completely different)", "And Now, For \"Something\" Completely Different"],
#		[r"&str_capitalize(and now for SOMETHING completely different, smart_en)", "And Now for Something Completely Different"],
#		[r"&str_capitalize(SPAM of %artist% With parrot, smart_en)", "Spam of Artist with Parrot"],
#		[r"&str_capitalize(i'd love spam, smart_en)", "I'd Love Spam"],
#		[r"&str_substring(brave sir robin, 4, 11)", "e sir r"],
#		[r"&str_substring(brave sir robin, -42, 42)", "brave sir robin"],
#		[r"&str_substring(brave sir robin, 2, -2)", "ave sir rob"],
#		[r"&str_substring(brave sir robin, 42, -42)", ""],
#		[r"&str_substring(brave sir robin, -42, 11)", "brave sir r"],
#		[r"&str_substring(brave sir robin, 4, 42)", "e sir robin"],
#		[r"&str_substring(brave sir robin, 8, 8)", ""],
#		[r"[%titre%|no_title]", "no_title"],
#		[r"&str_lpadd(spam,am, 11)", "spamamamama"],
#		[r"&str_lfill(spam,ma, 11)", "spammamamam"],
#		[r"&num_multiply(0.3f,3.1,2.2,1.3)", "8.866"],
#		[r"&num_multiply(d,3.1,2.2,1.3)", "8"],
#		[r"&num_multiply(3.1,2.2,1.3)", "8"],
#		[r"&num_multiply(spam,3.1,2.2,burp,1.3)", "8"],
#		[r"&num_add(0.3f,3.3,2.2,1.7)", "7.200"],
#		[r"&num_add(d,3.3,2.2,1.7)", "7"],
#		[r"&num_add(3.3,2.2,1.7)", "7"],
#		[r"&num_add(spam,3.3,2.2,burp,1.7)", "7"],
#		[r"&set_multi(01/20,/,tracknumber,totaltrack)[%tracknumber%] over [%totaltrack%]", "01 over 20"],

	]


	tag_ = {
		"title" : "TITLE",
		"artist" : "ARTIST",
		"album" : "ALBUM",
		"trackartist" : "TRACKARTIST",
		"tracknumber" : "TRACKNUMBER",
		"__true__" : "%__true__%",
		"__tab__" : "\t"
	}

	a = 0
	H = PrettyTag()
	
	s = 0
	
	for t in u :
		
		o = H.format(t[0], tag_=tag_)
		
		if o == t[1] :
			print("\ntest %02d\t. Ok ." % (a,))
			s += 1
		else :
			print("\ntest %d\t! Failed !" % (a,))
		print("format string: %s" % (t[0]))
		print("expected:", t[1])
		print("obtained:", o)
		a += 1
		
	print("\npassed %02d test(s) over %02d" % (s, a))
