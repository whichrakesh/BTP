import os,re
project_path = '/home/rakesh/quantlib-master'
for root, dirs, files in os.walk(project_path):
    for name in files:
		if(name.endswith('.c')):			
			filename = os.path.join(root,name)
			# print filename
			f = open(filename,'r')
			name_printed = False
			line = f.readline()
			while line:
				searchObj = re.search(r'for\s*\([^;]*;[^;]*;[^)]*\)',line)								
				if searchObj and not line.strip(' \t').startswith(r'//'):
					if not name_printed:
						print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^', filename , '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
						name_printed = True
					count = 0
					while '{' not in line:
						if line.strip(' \t\n').endswith(';'):
							break
						print line.strip('\n')						
						line = f.readline()	
					print line.strip('\n')	
					opening = re.findall(r'{',line)
					count = count + len(opening	)
					while(line and count != 0):
						line = f.readline()
						print line.strip('\n')
						opening = re.findall(r'{',line)
						count = count + len(opening)
						closing = re.findall(r'}',line)
						count = count - len(closing)
					print 	
				line = f.readline()
			f.close()
			if name_printed:
				print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
