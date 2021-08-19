from collections import defaultdict

dict = []
#take out all triples with marriage relation
intended_triples = []
#word = 'symmtery_sibling'
word = 'symm'
type = 'valid.txt'
all_lines = []
with open('../wn18/Inductive/Inductive_v4/' + type , "r")as a_file:
	for line in a_file:
		j = line.split()
		if(len(j)>2):
			j[2] = j[2].rstrip()
			all_lines.append(j)
			if(not (j[1] in dict)):
				dict.append(j[1])



print(len(all_lines))
print('writing Entities')			
numberOfEntities = []
c = 0
co = 0
#f1=open('../fb15k/Symmetry/numberOfEntities.'+type, 'w')
for v in all_lines:	
		#if c <10000:
	f_e = v[0]
	l_e = v[2]
	if not (f_e in numberOfEntities):
		numberOfEntities.append(f_e)
		#f1.write(f_e + '\n')
	if not (l_e in numberOfEntities):
		numberOfEntities.append(l_e)			
		#f1.write(l_e + '\n')	 		

print(len(numberOfEntities))

print('writing Relations')			
inverses = []
c = 0
co = 0
#f1=open('../fb15k/Symmetry/123relations'+type, 'w')
for g in all_lines:	
	#if c <10000:
	xe = g[1]
	#l_e = v[2]

	if not(xe in inverses):
		inverses.append(xe)
		#inverses.append(l_e)	
		#f1.write(f_e)
		#f1.write(l_e)	 		

print(len(inverses))