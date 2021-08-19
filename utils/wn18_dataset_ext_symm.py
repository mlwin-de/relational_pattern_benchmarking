
dict = []
dir = "../wn18/Original/text/"
symmetry = []
def extract(fileName):
	symmetry = []
	with open(dir + fileName, "r")as a_file:
		for line in a_file:
			j = line.split()
			if(not (j[1] in dict)):
				dict.append(j[1])
			if("_derivationally_related_form" in j[1] or "also_see" in j[1] or "similar_to" in j[1]):
				symmetry.append(line)
		if(len(symmetry)>1):
			f1=open('../wn18/symmetry/' + fileName, 'w')
			for k in symmetry:
				f1.write(k)

extract('train.txt')

extract('test.txt')

extract('valid.txt')
