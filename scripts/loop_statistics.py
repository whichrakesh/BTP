import os,re
project_path = '/home/rakesh/Dropbox/Study/Sem-7/BTP-I/quantlib-master'
total_for = 0
total_for_with_cond = 0
total_nested_for = 0
total_while = 0
total_while_with_cond = 0
stmts_count_over_all_file = 0
stmts_inside_loop_count_over_all_file = 0
print "filename: for_count for_with_cond_count nested_for_count while_count while_with_cond_count stmts_inside_loop total_stmts"	
for root, dirs, files in os.walk(project_path):
    for name in files:
		if(name.endswith('.cpp')):			
			filename = os.path.join(root,name)
			f = open(filename,'r')
			name_printed = False
			for_count = 0
			for_with_cond_count = 0
			nested_for_count = 0
			while_with_cond_count = 0
			while_count = 0
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
						opening = re.findall(r'{',line)
						count = count + len(opening)
						closing = re.findall(r'}',line)
						count = count - len(closing)
					if (if_present or switch_present):
						for_with_cond_count = for_with_cond_count + 1
					if nested_for :
						nested_for_count += 1
				else:	
					searchObj = re.search(r'while\s*\([^)]*\)',line)
					if searchObj and not line.strip(' \t').startswith(r'//'):
						while_count = while_count + 1
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
							opening = re.findall(r'{',line)
							count = count + len(opening)
							closing = re.findall(r'}',line)
							count = count - len(closing)
						if (if_present or switch_present):
							while_with_cond_count = while_with_cond_count + 1	
					else:
						if ';' in line:
							total_stmts += 1
				line = f.readline()
			print filename.replace(project_path,""),  for_count, for_with_cond_count, nested_for_count,  while_count, while_with_cond_count, stmts_inside_loop , total_stmts	
			total_for += for_count
			total_while += while_count
			total_for_with_cond +=  for_with_cond_count
			total_nested_for += nested_for_count
			total_while_with_cond += while_with_cond_count
			stmts_inside_loop_count_over_all_file += stmts_inside_loop
			stmts_count_over_all_file += total_stmts
			f.close()

print "\n\n\n"
print "total for:", total_for 
print "for with cond:", total_for_with_cond
print "total nested for:", total_nested_for
print "total while:" , total_while
print "while with cond:" , total_while_with_cond
print "statements inside loop:", stmts_inside_loop_count_over_all_file
print "total statements:", stmts_count_over_all_file