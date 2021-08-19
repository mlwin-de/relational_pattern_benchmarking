from collections import defaultdict
from os import write

dict = []
#take out all triples with marriage relation
intended_triples = []
#word = 'symmtery_sibling'
word = 'symm'
type = 'valid'
all_lines = []
train_entities = []
valid_entities = []
test_entities = []
#gets a line and appends possible and appends its possible inverses 
def InverseUtil(lineEntry, allLines, inverses):
	first_entity = lineEntry[0]
	second_entity = lineEntry[2]
	kj = [x for x in allLines if (x[0] == second_entity and x[2] == first_entity and x[0] != x[2] and lineEntry[1] != x[1])]
	#there are many with more than one inverse form, just ignore
	if(len(kj) == 1):
		line_1 = first_entity + '\t' + lineEntry[1] + '\t' + second_entity + '\n'
		line_2 = kj[0][0] + '\t' + kj[0][1] + '\t' + kj[0][2] + '\n'
		if not(line_1 in inverses or line_2 in inverses):
			inverses.append(line_1)
			inverses.append(line_2)
									
#region finding inverse from the dataset
not_in_train_inverse_lines = []
train_inverse_lines = []
def GetInverse(mode = 'train'):
	print('writing inverse triples')			
	inverses = []
	c = 0
	co = 0
	with open('fb15k/original/' + mode + '.txt', "r") as file:
		all_lines  = file.readlines()
		all_lines = [line.split() for line in all_lines]
		if mode == 'train':
			train_entities = []
			max = 15000
		else:
			max = 0

	print(len(all_lines))
	for entry in all_lines:	
		if c < max:			
			first_entity = entry[0]
			second_entity = entry[2]
			InverseUtil(entry, all_lines, inverses)
			if mode == 'train':
				train_inverse_lines.append(entry)
				if first_entity not in train_entities:
					train_entities.append(first_entity)
				if second_entity not in train_entities:
					train_entities.append(second_entity)
			print(c)		
			c = c + 1
		else:
			if mode == 'train':
				#valid/test files are too small; consider records from the ORIGINAL train file (THAT ARE NOT BEING ADDED TO THE INVERSE TRAIN)
				not_in_train = [line for line in all_lines[max:] if line not in train_inverse_lines]
				print('not in train', len(not_in_train))
				not_in_train_inverse_lines.extend(not_in_train)
				print('train_inverse', len(train_inverse_lines))				
				print('not in train inverse', len(not_in_train_inverse_lines))
				#check, none of the lines in not_in_train_inverse_lines should appear in train_inverse_lines	
				#result =  any(elem in train_inverse_lines for elem in not_in_train_inverse_lines)
				#print('Is there any entry in train_inverse_lines and also in NOT_inverse_lines ? ' , result)
				break

	#for test/valid read from train_inverse_lines now
	if mode != 'train':
		c = 0
		sub = int(len(not_in_train_inverse_lines)/2)
		if(mode == 'valid'):		
			extended_inverse_dataset = not_in_train_inverse_lines[0:sub]
		elif mode == 'test':
			extended_inverse_dataset = not_in_train_inverse_lines[(sub+1):]
		for entry in extended_inverse_dataset:
			if c >= 4000:
				break
			InverseUtil(entry, extended_inverse_dataset, inverses)
			print (c , '/', len(extended_inverse_dataset))
			print('valid - inverse - length ', len(inverses))
			c = c + 1
			
	return inverses

def GetSymm(type = 'train'):
	symm = []
	with open('fb15k/original/' + type + '.txt', "r")as a_file:
		for line in a_file:
			all_lines.append(line)
			j = line.split()
			if("people/sibling_relationship/sibling" in j[1]
			or "spouse_s./people/marriage/spouse" in j[1]
			or "base/popstra/friendship/participant" in j[1]):
				symm.append(line)	
				if type == 'train':
					if j[0] not in train_entities:
						train_entities.append(j[0])
					if j[2].rstrip() not in train_entities:
						train_entities.append(j[2].rstrip())
#				elif type == 'valid':
#					if j[0] not in valid_entities:
#						valid_entities.append(j[0])
#					if j[2].rstrip() not in valid_entities:
#						valid_entities.append(j[2].rstrip())
#				else:
#					if j[0] not in test_entities:
#						test_entities.append(j[0])		
#					if j[2].rstrip() not in test_entities:
#						test_entities.append(j[2].rstrip())	

	return symm

def dataSetLines(dataset, type = 'train'):
	lines = []
	if type == 'train':
		train_entities = []
	if dataset == 'Symm':
		lines = GetSymm(type)
	elif dataset == 'Inverse':
		lines = GetInverse(type)
	return lines

path = 'fb15k/fixedDS/'
type = ['train', 'valid']
d_test_entities = []
d_valid_entities = []
dataset = ['Symm', 'Inverse']
for dS in dataset:
	for i in type:
		lines = dataSetLines(dS, i)
		with open(path + '/' + dS + '/'+ i + '.txt', 'w') as file:
			if i == 'train':
				#write all lines
				file.write(''.join(lines))
			else:
				for line in lines:
					j = line.split()
					#ONLY write the line if both the entities are in training
					if j[0] in train_entities and j[2].rstrip() in train_entities:
						file.write(line)
						if type == 'valid':
							if j[0] not in d_valid_entities:
								d_valid_entities.append(j[0])
							if j[2].rstrip() not in d_valid_entities:
								d_valid_entities.append(j[2].rstrip())
						else:
							if j[0] not in d_test_entities:
								d_test_entities.append(j[0])		
							if j[2].rstrip() not in d_test_entities:
								d_test_entities.append(j[2].rstrip())		

	result =  all(elem in train_entities for elem in d_valid_entities)
	print('all valid entities for dataset ' + dS + ' in train_entities -->', result)
	result =  all(elem in train_entities for elem in d_test_entities)
	print('all test entities for dataset ' + dS + ' in train_entities  -->', result)


# f1=open('./fb15k/unique_relations.txt', 'w')
# for l in relations:
# 	f1.write(l+'\n')
# #f1=open('./fb15k/relations.txt', 'w')
# #for k in dict:
# 	#f1.write(k + "\n")

# #print(len(intended_triples))


#dicti = resolve_entities(intended_triples)
#write_to_file(inverses)

#dicti = resolve_entities(intended_triples)
#write_to_file(intended_triples)


# f = open('./fb15k/entities_'+word+'.txt', 'w')
# for value in dicti.values():
# 	f.write(value+'\n')

#copying anti-symm from inverses
#only copying alternate lines
# count = 0
# anti_symm_rows = []
# with open('../fb15k/inverse/new/'+type+'_'+word+'.txt', "r")as f1, open('../fb15k/anti-symm/new/'+type+'_anti-symm.txt', 'w') as f2:
# 	for line in f1:
# 		#count = count + 1
# 		row = [x for x in anti_symm_rows if (x.split()[0] == line.split()[2] and x.split()[2] == line.split()[0]) or (x.split()[0] == line.split()[0] and x.split()[2] == line.split()[2])]
# 		if(count % 2 == 0 and len(row) == 0):
# 			anti_symm_rows.append(line)
# 			#print(row, str(len(row)))
# 		count = count + 1
# 	for line in anti_symm_rows:
# 		j = line.split()
# 		if(not (j[0] == j[2].rstrip())):
# 			f2.write(line)
# 	print(len(anti_symm_rows))