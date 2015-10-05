import os,re
filename = '/home/rakesh/Dropbox/Study/Sem-7/BTP-I/for_loop_extracted/quantlib.txt'
f = open(filename,'r')
toprint = ""
array_found = False

def findForLoopBody(line, basecount):
	global toprint, array_found
	arraydict = dict()
	count = basecount
	start = ""
	for i in range(basecount):
		start += '\t'	
	while '{' not in line:
		if line.strip(' \t\n').endswith(';'):
			break
		# print line.strip('\n')
		line = f.readline()
	# print line.strip('\n')	
	opening = re.findall(r'{',line)
	count = count + len(opening)			
	toprint += start + "{\n"
	while(line and count != basecount):
		line = f.readline()

		#checking for loops inside loop
		searchObj = re.search(r'for\s*\(([^;]*);([^;]*);([^)]*)\)',line)								
		if searchObj and not line.strip(' \t').startswith(r'//'):
			toprint += start + "\tloop info: " + searchObj.group(1) + " " + searchObj.group(2) + " " + searchObj.group(3)	+ "\n"
			findForLoopBody(line,count)
			line = f.readline()
		arrayrefs = re.findall(r'([a-zA-Z_][a-zA-Z0-9_.]+)((?:\[[^\]]\])+)', line)
		if(len(arrayrefs)):
			array_found = True
			# toprint += "\t" + line.strip(' \t')
			for (key,value) in arrayrefs:
				if(arraydict.has_key(key)):
					arraydict[key].append(value)
				else:
					arraydict[key] = [value]
			# toprint += "\tarray references: " + str(arrayrefs) + "\n\n"
		# print line.strip('\n')

		opening = re.findall(r'{',line)
		count = count + len(opening)
		closing = re.findall(r'}',line)
		count = count - len(closing)
	# toprint += "}\n"		
	if(array_found):
		print toprint,
		print start + "-----------------------------------------------"
		print start + "array table"
		for key in arraydict.keys():
			print start + key, '->' , str(arraydict[key])
		print start + "-----------------------------------------------"	
		print start + "}"
	toprint = ""	


line = f.readline()
while line:
	if line.startswith("^^"):
		print line
	array_found = False	
	searchObj = re.search(r'for\s*\(([^;]*);([^;]*);([^)]*)\)',line)								
	if searchObj and not line.strip(' \t').startswith(r'//'):
		toprint += "loop info: " + searchObj.group(1) + " " + searchObj.group(2) + " " + searchObj.group(3)	+ "\n"
		findForLoopBody(line,0)
		if(array_found):
			print 
	line = f.readline()

f.close()

