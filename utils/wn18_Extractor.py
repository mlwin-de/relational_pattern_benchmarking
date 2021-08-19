from collections import defaultdict

dict = []
#take out all triples with marriage relation
intended_triples = []
#word = 'symmtery_sibling'
word = 'symm'
type = 'valid.txt'
all_lines = []
with open('../fb15k/original/' + type , "r")as a_file:
	for line in a_file:
		j = line.split()
		if(len(j)>2):
			j[2] = j[2].rstrip()
			all_lines.append(j)
			if(not (j[1] in dict)):
				dict.append(j[1])
		# if("people/sibling_relationship/sibling" in j[1]):
		# #if(word in j[1]):
		# 	intended_triples.append(line)

#region finding inverse from the dataset
print(len(all_lines))
print('writing inverse triples')			
inverses = []
c = 0
co = 0
f1=open('../fb15k/Inverse/123'+type, 'w')
for v in all_lines:	
	if c <10000:
		f_e = v[0]
		l_e = v[2]
		kj = [x for x in all_lines if (x[0] == l_e and x[2] == f_e)]
		#there are many with more than one inverse form, just ignore
		if(len(kj) == 1):
			l1 = f_e + '\t' + v[1] + '\t' + l_e + '\n'
			l2 = kj[0][0] + '\t' + kj[0][1] + '\t' + kj[0][2] + '\n'
			if not(l1 in inverses or l2 in inverses):
				inverses.append(l1)
				inverses.append(l2)	
				f1.write(f_e + '\t' + v[1] + '\t' + l_e + '\n')
				f1.write(kj[0][0] + '\t' + kj[0][1] + '\t' + kj[0][2] + '\n')	 		
					#print(l1)
					#print(l2)	
					#co = co+1
					#print(co)
				#else:
			c = c + 1
print(len(inverses))
# c = 0
# all_lines = all_lines[10000:]
# inverses_2 = []
# f1 = open('../fb15k/inverse/inverse_2.txt','w')
# for v in all_lines:	
# 	if c <10000:
# 		f_e = v[0]
# 		l_e = v[2]
# 		kj = [x for x in all_lines if (x[0] == l_e and x[2] == f_e)]
# 		#there are many with more than one inverse form, just ignore
# 		if(len(kj) == 1):
# 			l1 = f_e + '\t' + v[1] + '\t' + l_e + '\n'
# 			l2 = kj[0][0] + '\t' + kj[0][1] + '\t' + kj[0][2] + '\n'
# 			if not(l1 in inverses or l2 in inverses) and not (l1 in inverses_2 or l2 in inverses_2):
# 				inverses_2.append(l1)
# 				inverses_2.append(l2)	
# 				f1.write(l1)
# 				f1.write(l2)	 		
# 					#print(l1)
# 					#print(l2)	
# 					#co = co+1
# 					#print(co)
# 				#else:
# 			c = c + 1
# print(len(inverses_2))

