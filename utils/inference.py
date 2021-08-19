from collections import defaultdict

dict = []
#take out all triples with marriage relation
intended_triples = []
#word = 'symmtery_sibling'
word = 'inverses'
type = 'valid'
all_lines = []
with open('../fb15k/original/valid.txt', "r")as a_file:
	for line in a_file:
		j = line.split()
		if(len(j)>2):
			j[2] = j[2].rstrip()
			all_lines.append(j)
			if(not (j[1] in dict)):
				dict.append(j[1])

print('writing inference triples')			
inferences = []
f1=open('../fb15k/inference/'+type+'_inference.txt', 'w')
c = 0
for v in all_lines:
	if(c < 10000):
		f_e = v[0]
		l_e = v[2]
		kj = [x for x in all_lines if (x[0] == f_e and x[2] == l_e and not (v[1] == x[1]))]
		#there are many with more than one inverse form, just ignore
		if(len(kj) == 1):
			inferences.append(f_e + '\t' + v[1] + '\t' + l_e + '\n')
			inferences.append(kj[0][0] + '\t' + kj[0][1] + '\t' + kj[0][2] + '\n')
			f1.write(f_e + '\t' + v[1] + '\t' + l_e + '\n')
			f1.write(kj[0][0] + '\t' + kj[0][1] + '\t' + kj[0][2] + '\n')
	c = c + 1

all_lines = []
misses = defaultdict(int)
i = 1
with open('../fb15k/inference/'+type+'_inference.txt', "r")as a_file:
	temp = ''
	for line in a_file:					
		j = line.split()
		if(len(j)>2):
			j[2] = j[2].rstrip()
			all_lines.append(j)
kp = []
hits = defaultdict(int)
with open('../fb15k/inference/'+type+'_inference.txt', "r")as a_file:
	while True:
		l1 = a_file.readline().split()
		l2 = a_file.readline().split()	
		#misses[s] > 0 means already visited these relationships			
		if (not (l2) or (len(l1) < 3 or len(l2) < 3)):
			break
		s1 = l1[1] + '***' + l2[1]
		s2 = l2[1] + '***' + l1[1]
		if misses[s1] > 0 or misses[s2] > 0: 
			continue
		i = 0
		if l1[0] == l2[0] and l1[2] == l2[2] and not(l1[1] == l2[1]):
			coupled_lines = [x for x in all_lines if (x[1] == l1[1] or x[1] == l2[1])]
			if len(coupled_lines)>0:
				for ind_line in coupled_lines:
					existing_doubles = [x for x in coupled_lines if not(x[1] == ind_line[1]) and x[0]== ind_line[0] and x[2] == ind_line[2]]
					if len(existing_doubles) == 0:
						#print(ind_line[0] + ' ' + ind_line[2] + ' ' + l1[1]+'  ' + l2[1])
						misses[s1] = misses[s1] + 1
					else:
						hits[s1] = hits[s1] + 1


#f1=open('./fb15k/relations_hits_misses.txt', 'w')
rel_scores = {}
import csv
with open('../fb15k/inference/'+type+'_relations_hits_misses.csv', mode='w') as inf_file:
	file_writer = csv.writer(inf_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for (k,v) in hits.items():
		jk = k.split('***')
		file_writer.writerow([jk[0], jk[1],  str(v),  str(misses[k]), str(v/(v + misses[k]))])
		rel_scores[k] = v/(v + misses[k])
		#f1.write(jk[0] + '->' + jk[1] + '\t' + str(v) +'\t'+ str(misses[k])+'\n')
f1=open('../fb15k/inference/'+type+'_inference_filtered.txt', 'w')
for k,v in rel_scores.items():
	i =0
	if(v >= 0.9):
		coupled_relations = k.split('***')
		while ((i + 1) < len(all_lines)):
			first_line = all_lines[i]
			second_line = all_lines[i+1]
			if not second_line:
				break
			if ((first_line[1] == coupled_relations[0] and second_line[1] == coupled_relations[1])
			or (first_line[1] == coupled_relations[1] and second_line[1] == coupled_relations[0])):
				f1.write(all_lines[i][0] + '\t' + all_lines[i][1] + '\t' + all_lines[i][2] + '\n')
				f1.write(all_lines[i + 1][0] + '\t' + all_lines[i + 1][1] + '\t' + all_lines[i + 1][2]+'\n')
			i = i + 2
	else:
		continue