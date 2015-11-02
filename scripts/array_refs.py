import os,re, sys
if len(sys.argv) < 2:
	sys.exit("please enter the filename to be parsed as argument.")

filename = os.path.abspath(sys.argv[1]) #'/home/rakesh/Dropbox/Study/Sem-7/BTP-I/for_loop_extracted/quantlib.txt'
print 'filename:' , filename 
f = open(filename,'r')

toprint = ""
array_found = False
line_num = 0

total_ldes = 0
distinct_ldes = 0
max_ldes_for_a_loop = 0
total_array_refs = 0
normalized_array_refs = 0
maximum_loop_nest = 0
total_read_count = 0
total_write_count = 0
var_count_map = dict()

def countIndVars(exp,ind_vars):
	ids = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*',exp)
	count = 0
	for id in ids:
		if(id in ind_vars):
			count += 1
	return count 
			
def replace_fun1(id,ind_vars):
	if id in ind_vars:
		return id + '1'
	else :
		return id	
	

def replace_fun2(id,ind_vars):
	if id in ind_vars:
		return id + '2'
	else :
		return id

def findForLoopBody(line, basecount, nest_level, induction_vars):
	global toprint, array_found, line_num, total_ldes, distinct_ldes, total_array_refs, normalized_array_refs, maximum_loop_nest		
	maximum_loop_nest = max(maximum_loop_nest, nest_level)
	count = basecount
	start = ""
	for i in range(basecount):
		start += '\t'	
	while '{' not in line:
		comment_pos = line.find('//')
		if comment_pos != -1:
			line = line[0:comment_pos]
		if line.strip(' \t\n\\').endswith(';'):
			break
		# print line.strip('\n')
		line = f.readline()
	# print line.strip('\n')	
	opening = re.findall(r'{',line)
	count = count + len(opening)	
	closing = re.findall(r'}',line)
	count = count - len(closing)		
	if(count > basecount):
		toprint += start + "{\n"
	while(line and count > basecount):
		line = f.readline()

		#checking for loops inside loop
		searchObj = re.search(r'for\s*\(([^;]*);([^;]*);([^)]*)\)',line)								
		if searchObj and (line.find(r'//') == -1 or line.find(r'//') > line.find(r'for')):
			toprint += start + "\tloop info: " + searchObj.group(1) + " " + searchObj.group(2) + " " + searchObj.group(3)	+ "\n"
			iterator_exp = searchObj.group(3)
			iterators = re.findall(r'(\+\+|--)?[ \t]*([a-zA-Z_][a-zA-Z0-9_]*)[ \t]*((?:<<|>>|\+\+|--|[+\-*/%\&\^\|])?=*)',iterator_exp)		
			ind_vars = induction_vars
			if(len(iterators)):
				for (inc_op,identifier,right_op) in iterators:
					if((inc_op != '') or (right_op == '++') or (right_op == '--') or (right_op != '' and right_op != '==' and right_op.endswith('='))):					
						if identifier not in ind_vars:
							ind_vars.append(identifier)
			toprint += start + "\tinduction variable: " + str(ind_vars) + '\n'
			count = count - findForLoopBody(line,count,nest_level+1,ind_vars)
			line = f.readline()
		arrayrefs = re.findall(r'(\+\+|--)?[ \t]*([a-zA-Z_][a-zA-Z0-9_.]*)((?:\[[^\[\]]+\])+)(\.[a-zA-Z_][a-zA-Z0-9_.]*)*[ \t]*((?:<<|>>|\+\+|--|[+\-*/%\&\^\|])?=*)', line)
		if(len(arrayrefs)):
			total_array_refs += len(arrayrefs)
			array_found = True
			line_num += 1
			# toprint += "\t" + line.strip(' \t')
			toprint += start+'L'+str(line_num) + ': '
			for (inc_op,array_name,expr,data_member,right_op) in arrayrefs:
				if((inc_op != '') or (right_op == '++') or (right_op == '--') or (right_op != '' and right_op != '==' and right_op.endswith('='))):
					rw_type = 'w'
				else:
					rw_type = 'r'				
				ids = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*',expr);

				normalized = "normalized"
				for identifier in ids:
					if identifier not in induction_vars:
						normalized = "not normalized"
				if(normalized == "normalized"):
					normalized_array_refs += 1
				value = (expr, rw_type, normalized, induction_vars, line_num)
				if(arraydict.has_key(array_name)):
					arraydict[array_name].append(value)
				else:
					arraydict[array_name] = [value]
				toprint += '(' + inc_op+array_name+expr+data_member+right_op + ',' + rw_type + ') '
			toprint += '\n'					
		# print line.strip('\n')		
		opening = re.findall(r'{',line)
		count = count + len(opening)
		closing = re.findall(r'}',line)
		count = count - len(closing)
		# if(opening or closing):
		# 	print bfore, count , opening, closing, line, 
	# toprint += "}\n"		
	if(array_found):
		print toprint, 		
		print start + "}"
	toprint = ""	
	return basecount - count

line = f.readline()
while line:
	arraydict = dict()
	if line.startswith("^^"):
		print line
	array_found = False	
	searchObj = re.search(r'for\s*\(([^;]*);([^;]*);([^)]*)\)',line)								
	if searchObj and (line.find(r'//') == -1 or line.find(r'//') > line.find(r'for')):
		toprint += "loop info: " + searchObj.group(1) + " " + searchObj.group(2) + " " + searchObj.group(3)	+ "\n"
		iterator_exp = searchObj.group(3)
		iterators = re.findall(r'(\+\+|--)?[ \t]*([a-zA-Z_][a-zA-Z0-9_]*)[ \t]*((?:<<|>>|\+\+|--|[+\-*/%\&\^\|])?=*)',iterator_exp)		
		ind_vars = []
		if(len(iterators)):
			for (inc_op,identifier,right_op) in iterators:
				if((inc_op != '') or (right_op == '++') or (right_op == '--') or (right_op != '' and right_op != '==' and right_op.endswith('='))):					
					ind_vars.append(identifier)
		toprint += "induction variable: " + str(ind_vars) + '\n'
		findForLoopBody(line,0,1,ind_vars)
		if(array_found):
			print "array table"	
			print "-----------------------------------------------"		
			LDEs = set()
			for key in arraydict.keys():
				read_count = 0
				write_count = 0				
				for i in xrange(len(arraydict[key])):
					value = arraydict[key][i]
					expr,rw_type,normalized, ind_vars, line_num = value
					brackets_count = expr.count('[')					
					if(normalized):
						expressions = re.findall(r'\[([^\]]+)\]',expr)

						re_exp1 = []
						re_exp12 = []
						for exp in expressions:
							re_exp1.append(re.sub(r'[a-zA-Z_][a-zA-Z0-9_]*', lambda x: replace_fun1(x.group(0),ind_vars), exp))
							re_exp12.append(re.sub(r'[a-zA-Z_][a-zA-Z0-9_]*', lambda x: replace_fun2(x.group(0),ind_vars), exp))							
						for j in xrange(i,len(arraydict[key])):
							value2 = arraydict[key][j]
							expr2,rw_type2,normalized2, ind_vars2, line_num2 = value2
							if(rw_type != rw_type2  or rw_type == 'w'):
								exps2 = re.findall(r'\[([^\]]+)\]',expr2)
								re_exp2 = []
								re_exp21 = []
								for exp in exps2:
									re_exp2.append(re.sub(r'[a-zA-Z_][a-zA-Z0-9_]*', lambda x: replace_fun2(x.group(0),ind_vars2), exp))
									re_exp21.append(re.sub(r'[a-zA-Z_][a-zA-Z0-9_]*', lambda x: replace_fun1(x.group(0),ind_vars2), exp))									
								sep = ''	
								LDE = ''
								LDE2 = ''
								for j in xrange(min(len(re_exp1),len(re_exp2))):
									LDE += sep + re_exp1[j] + '=' + re_exp2[j]
									LDE2 += sep + re_exp21[j] + '=' + re_exp12[j] 
									sep = ','
								# print LDE, "added"
								# print LDEs
								if(LDE2 not in LDEs):
									LDEs.add(LDE)

					if(rw_type == 'r'):
						read_count += 1
					else :
						write_count += 1
				print  key, '->' , str(arraydict[key])
				lde_count = brackets_count * (read_count*write_count+(write_count*(write_count+1))/2)
				total_read_count += read_count
				total_write_count += write_count				
				total_ldes += lde_count
				print 'LDEs formed:' + str(lde_count)+ '\n'	
			print "distinct LDEs:"
			distinct_ldes += len(LDEs)
			max_ldes_for_a_loop = max(max_ldes_for_a_loop, len(LDEs))
			for LDE in LDEs:
				print LDE				
				ids = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*',LDE)
				if var_count_map.has_key(len(ids)):
					var_count_map[len(ids)] += 1
				else :
					var_count_map[len(ids)] = 1
			print  "#########################################################################################"	 
	line = f.readline()


print "***************************************stats******************************************"
print "total_ldes:" , total_ldes
print "distinct_ldes:", distinct_ldes
print "maximum_ldes_for_a_loop:", max_ldes_for_a_loop
print "total_array_refs:", total_array_refs
print "normalized_array_refs:", normalized_array_refs
print "maximum_loop_nest:", maximum_loop_nest
print "total_read_count:" , total_read_count
print "total_write_count:", total_write_count
print "n-variable_ldes:", var_count_map
f.close()