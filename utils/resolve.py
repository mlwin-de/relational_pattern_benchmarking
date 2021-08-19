def resolve_entities(triples):
	#take out unique list of entities that exist in the file
	#which would be then resolved for their names from freebase
	entities = []
	c = 0
	if(len(triples)>1):
		#f1=open('./fb15k/'+word+'_tris_only.txt', 'w')
		for k in triples:
			if(not(k.split('\t')[0] in entities)):
				entities.append(k.split('\t')[0].rstrip())
			if(not(k.split('\t')[2] in entities)):
				entities.append(k.split('\t')[2].rstrip())			
			#f1.write(k)

	print('resolving entities')
	dicti = {}
	i =0

	if(len(triples)>1):
		with open('./mid2name.tsv', 'r') as a_file:
			a_lines = a_file.readlines()				
			for k in entities:
				#print(k)
				flag = 0
				l = 0
				#a_lines = a_file.readlines()
				while(l < len(a_lines) and not flag):
					line = a_lines[l]
					splitted_line = line.split()
					#print(k +'\t'+ splitted_line[0]+'\n\n')
					if(k in splitted_line[0]):
						if(len(splitted_line)>1):		
							flag = 1
							jk = ' '.join(splitted_line[1:])
							dicti[k] = jk							
					l=l+1
				#l = 0	
				#a_file.seek(0)		
				if(flag == 0):
					c = c+1
					print('not found ' + k)
				i = i +1
				print('resolved', str(i), '/',str(len(entities)))
	print('number of unresolved entities : ' + str(c))
	return dicti
lines = []
with open('./fb15k/inverse/new/inverse.txt', "r")as a_file:
	for line in a_file:
		lines.append(line)

def write_to_file(triples):
	print('writing to file')
	f2 = open('./fb15k/inverse_withNames.txt', 'w')
	for mar_line in triples:
		kj = mar_line.split()
		if(kj[0] in dicti and kj[2] in dicti):
			line = dicti[kj[0]] + ' ' +kj[1]+' ' + dicti[kj[2]]+'\n'
			f2.write(line)
		else:
			print(kj)		
dicti = resolve_entities(lines)
write_to_file(lines)