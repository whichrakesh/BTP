import os,re,sys
if len(sys.argv) < 2:
	print "python loop_statistics.py [project_path]"
	sys.exit(0)

project_path = sys.argv[1]
total_for = 0
total_for_with_if = 0
total_for_with_switches = 0
total_for_with_array_refs = 0
total_for_with_function_calls = 0
total_nested_for = 0
total_while = 0
total_while_with_if = 0
total_while_with_switches = 0
total_while_with_array_refs = 0
total_while_with_function_calls = 0
stmts_count_over_all_file = 0
stmts_inside_loop_count_over_all_file = 0
print "filename for_count for_with_if_count for_with_switch_count for_with_array_references_count for_with_function_calls_count nested_for_count while_count while_with_if_count while_with_switch_count while_with_array_references_count while_with_function_calls_count stmts_inside_loop total_stmts"	
for root, dirs, files in os.walk(project_path):
    for name in files:
		if(name.endswith('.c') or name.endswith('.cpp')):			
			filename = os.path.join(root,name)
			f = open(filename,'r')
			name_printed = False
			for_count = 0
			for_with_if_count = 0
			for_with_switch_count = 0
			for_with_array_references_count = 0
			for_with_function_calls_count = 0
			nested_for_count = 0
			while_count = 0			
			while_with_if_count = 0
			while_with_switch_count = 0
			while_with_array_references_count = 0
			while_with_function_calls_count = 0
			stmts_inside_loop = 0
			total_stmts = 0
			line = f.readline()
			while line:
				searchObj = re.search(r'for\s*\([^;]*;[^;]*;[^)]*\)',line)
				if searchObj and not line.strip(' \t').startswith(r'//'):
					for_count = for_count + 1	
					count = 0
					while '{' not in line:
						if line.strip(' \t\n').endswith(';'):
							break					
						line = f.readline()	
						if ';' in line:
							total_stmts += 1
							stmts_inside_loop += 1
					if_present = False
					switch_present = False	
					nested_for = False
					array_ref = False
					function_call = False
					opening = re.findall(r'{',line)
					count = count + len(opening	)
					while(line and count != 0):
						line = f.readline()
						if ';' in line:
							total_stmts += 1
							stmts_inside_loop += 1
						searchObj = re.search(r'if\s*\([^)]*\)',line)
						if searchObj and not line.strip(' \t').startswith(r'//'):							
							if_present = True
						searchObj = re.search(r'switch\s*\([^)]*\)',line)
						if searchObj and not line.strip(' \t').startswith(r'//'):
							switch_present = True
						searchObj = re.search(r'for\s*\([^;]*;[^;]*;[^)]*\)',line)
						if searchObj and not line.strip(' \t').startswith(r'//'):							
							nested_for = True
						searchObj = re.search(r'[a-zA-Z0-9]+\[[^\]]\]',line)							
						if searchObj and not line.strip(' \t').startswith(r'//'):							
							array_ref = True							
						searchObj = re.search(r'[a-zA-Z0-9]+\([^\)]\)',line)							
						if searchObj and not line.strip(' \t').startswith(r'//'):							
							function_call = True								
						opening = re.findall(r'{',line)
						count = count + len(opening)
						closing = re.findall(r'}',line)
						count = count - len(closing)
					if if_present:
						for_with_if_count += 1
					if switch_present:
						for_with_switch_count += 1						
					if nested_for :
						nested_for_count += 1
					if array_ref :
						for_with_array_references_count += 1
					if function_call :
						for_with_function_calls_count += 1		
				else:	
					searchObj = re.search(r'while\s*\([^)]*\)',line)
					if searchObj and not line.strip(' \t').startswith(r'//'):
						while_count = while_count + 1
						count = 0
						while '{' not in line:
							if ';' in line.strip(' \t\n'):
								break					
							line = f.readline()	
							if ';' in line:
								total_stmts += 1
								stmts_inside_loop += 1
						if_present = False
						switch_present = False	
						array_ref = False
						function_call = False
						opening = re.findall(r'{',line)
						count = count + len(opening	)
						while(line and count != 0):
							line = f.readline()
							if ';' in line:
								total_stmts += 1
								stmts_inside_loop += 1
							searchObj = re.search(r'if\s*\([^)]*\)',line)
							if searchObj and not line.strip(' \t').startswith(r'//'):
								if_present = True
							searchObj = re.search(r'switch\s*\([^)]*\)',line)
							if searchObj and not line.strip(' \t').startswith(r'//'):
								switch_present = True
							searchObj = re.search(r'[a-zA-Z0-9]+\[[^\]]\]',line)							
							if searchObj and not line.strip(' \t').startswith(r'//'):							
								array_ref = True							
							searchObj = re.search(r'[a-zA-Z0-9]+\([^\)]\)',line)							
							if searchObj and not line.strip(' \t').startswith(r'//'):							
								function_call = True		
							opening = re.findall(r'{',line)
							count = count + len(opening)
							closing = re.findall(r'}',line)
							count = count - len(closing)
						if if_present:
							while_with_if_count += 1
						if switch_present:
							while_with_switch_count += 1
						if array_ref :
							while_with_array_references_count += 1
						if function_call :
							while_with_function_calls_count += 1	
					else:
						if ';' in line:
							total_stmts += 1
				line = f.readline()
			print filename.replace(project_path,""),  for_count, for_with_if_count, for_with_switch_count,  for_with_array_references_count, for_with_function_calls_count,  nested_for_count,  while_count, while_with_if_count, while_with_switch_count, while_with_array_references_count, while_with_function_calls_count, stmts_inside_loop , total_stmts	
			total_for += for_count
			total_while += while_count
			total_for_with_if +=  for_with_if_count
			total_for_with_switches += for_with_switch_count
			total_for_with_function_calls += for_with_function_calls_count
			total_for_with_array_refs += for_with_array_references_count
			total_nested_for += nested_for_count
			total_while_with_if += while_with_if_count
			total_while_with_switches += while_with_switch_count
			total_while_with_array_refs += while_with_array_references_count
			total_while_with_function_calls += while_with_function_calls_count
			stmts_inside_loop_count_over_all_file += stmts_inside_loop
			stmts_count_over_all_file += total_stmts
			f.close()

print "\n\n\n"
print "total-for:", total_for 
print "for-with-if:", total_for_with_if , `total_for_with_if*100/total_for` + "%"
print "for-with-switches:" , total_for_with_switches, `total_for_with_switches*100/total_for` + "%"
print "for-with-array-references:" , total_for_with_array_refs, `total_for_with_array_refs*100/total_for` + "%"
print "for-with-function-calls:" , total_for_with_function_calls , `total_for_with_function_calls*100/total_for` + "%"
print "total-nested-for:", total_nested_for, `total_nested_for*100/total_for` + "%"

print
print "total-while:" , total_while
print "while-with-if:" , total_while_with_if, `total_while_with_if*100/total_while` + "%"
print "while-with-switches:" , total_while_with_switches , `total_while_with_switches*100/total_while` + "%"
print "while-with-array-references:" , total_while_with_array_refs, `total_while_with_array_refs*100/total_while` + "%"
print "while-with-function-calls:" , total_while_with_function_calls, `total_while_with_function_calls*100/total_while` + "%"

print 
print "total-statements:", stmts_count_over_all_file
print "statements-inside-loop:", stmts_inside_loop_count_over_all_file , `stmts_inside_loop_count_over_all_file * 100/ stmts_count_over_all_file` + "%"