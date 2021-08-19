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
count = 0
anti_symm_rows = []
with open('../fb15k/inverse/new/'+type, "r")as f1, open('../fb15k/anti-symm/123'+type, 'w') as f2:
	for line in f1:
		#count = count + 1
		row = [x for x in anti_symm_rows if (x.split()[0] == line.split()[2] and x.split()[2] == line.split()[0]) or (x.split()[0] == line.split()[0] and x.split()[2] == line.split()[2])]
		if(count % 2 == 0 and len(row) == 0):
			anti_symm_rows.append(line)
			#print(row, str(len(row)))
		count = count + 1
	for line in anti_symm_rows:
		j = line.split()
		if(not (j[0] == j[2].rstrip())):
			f2.write(line)
	print(len(anti_symm_rows))