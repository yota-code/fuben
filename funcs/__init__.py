import fnmatch
import os

print("*** loading fuben/funcs/__init__.py ***")

register = {}

from . import text
for i in text.register :
	register[i] = text.register[i]

#import numeric
#for i in numeric.register :
#	register[i] = numeric.register[i]

from . import logic
for i in logic.register :
	register[i] = logic.register[i]
	
print("*** loaded fuben/funcs/__init__.py ***")

