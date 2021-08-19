train_entitites = []
train_relations = []
train_lines = []
def readTrain(dataset, type):
    f1=open(dataset + '/'+type+'/train.txt', 'r')
    train_lines.clear()
    train_relations.clear()
    train_entitites.clear()
    all_lines = f1.readlines()
    train_lines.extend(all_lines)
    #print(train_lines[0:4])
    all_lines = [line.split() for line in all_lines]
    #print(train_lines[0:4])
    for line in all_lines:
        if line[0] not in train_entitites:
            train_entitites.append(line[0])
        if line[2].rstrip() not in train_entitites:
            train_entitites.append(line[2].rstrip())
        if line[1] not in train_relations:
            train_relations.append(line[1])
    print('train_lines', len(train_lines))
    print('train_relations', len(train_relations))
    print('train_entities', len(train_entitites))

def WriteTransductive(dataset, type, mode):
    #b_e = 0
    #print(train_lines[0:4])
    output_lines = []
    f1 = open(dataset + '/'+type+'/'+mode+'.txt', 'r')
    f2 = open(dataset + '/fixedDS/Transductive/'+type+'/'+mode+'.txt', 'w')
    all_lines = f1.readlines()
    print('total '+type +'_'+ mode + ' lines ' +str(len(all_lines)))
    all_lines = [line.split() for line in all_lines]
    for line in all_lines:
        #entities exiting in train_entities
        #relation exsiting in train_relations
        tempL = line[0] + '\t' + line[1] + '\t' + line[2] + '\n'
        if (line[0] in train_entitites and line[2].rstrip() in train_entitites and line[1] in train_relations):
            #the whole tuple should not appear in train 
            if tempL not in train_lines:
                f2.write(tempL)
                output_lines.append(tempL)
            else:
                print(tempL)
        #else:
            #b_e = b_e + 1
    print('extracted ' + type + '_'+mode +' lines '+ str(len(output_lines)))
    #print('b_e', b_e)

def WriteInductive(dataset, type, mode):
    #b_e = 0
    #print(train_lines[0:4])
    output_lines = []
    f1 = open(dataset + '/'+type+'/'+mode+'.txt', 'r')
    f2 = open(dataset + '/fixedDS/Inductive/'+type+'/'+mode+'.txt', 'w')
    all_lines = f1.readlines()
    print('total '+type +'_'+ mode + ' lines ' +str(len(all_lines)))
    all_lines = [line.split() for line in all_lines]
    for line in all_lines:
        #entities exiting in train_entities
        #relation exsiting in train_relations
        tempL = line[0] + '\t' + line[1] + '\t' + line[2] + '\n'
        if (line[0] not in train_entitites and line[2].rstrip() not in train_entitites and line[1] in train_relations):
            #the whole tuple should not appear in train 
            if tempL not in train_lines:
                f2.write(tempL)
                output_lines.append(tempL)
            else:
                print(tempL)
        #else:
            #b_e = b_e + 1
    print('extracted ' + type + '_'+mode +' lines '+ str(len(output_lines)))

def WriteSemiInductiveHeadTailBased(dataset, type, mode):
    output_lines = []
    f1 = open(dataset + '/'+type+'/'+mode+'.txt', 'r')
    f2 = open(dataset + '/fixedDS/Semi-Inductive-HeadOrTailBased/'+type+'/'+mode+'.txt', 'w')
    all_lines = f1.readlines()
    print('total '+type +'_'+ mode + ' lines ' +str(len(all_lines)))
    all_lines = [line.split() for line in all_lines]
    for line in all_lines:
        #entities exiting in train_entities
        #relation exsiting in train_relations
        tempL = line[0] + '\t' + line[1] + '\t' + line[2] + '\n'
        #either the head should not appear in the train_entities or the tail
        #tail exist
        tailExist =  line[0] not in train_entitites and line[2].rstrip() in train_entitites   
        #head exist
        headExist =  line[0] in train_entitites and line[2].rstrip() not in train_entitites   
        
        if ((tailExist or headExist) and line[1] in train_relations):
            if tempL not in train_lines:
                f2.write(tempL)
                output_lines.append(tempL)
            else:
                print(tempL)
    print('extracted ' + type + '_'+mode +' lines '+ str(len(output_lines)))

def WriteSemiInductiveCountBased(dataset, type, mode):
    output_lines = []
    #read all fully-inductive for this dataset
    ffInductive = open(dataset + '/fixedDS/Inductive/'+type+'/'+mode+'.txt', 'r')
    ind_lines = ffInductive.readlines()
    #ind_lines = [line.split() for line in ind_lines]
    ffTransductive = open(dataset + '/fixedDS/Transductive/'+type+'/'+mode+'.txt', 'r')
    tr_lines = ffTransductive.readlines()
    #tr_lines = [line.split() for line in tr_lines]
    print(len(ind_lines))
    #extend the ind_lines by adding all tr_lines so it becomes a list with half transductive half inductive 
    ind_lines.extend(tr_lines[0:len(ind_lines)])
    print(len(ind_lines))
    f2 = open(dataset +'/fixedDS/Semi-Inductive-CountBased/'+type+'/'+mode+'.txt', 'w') 
    for line in ind_lines:
        f2.write(line)

def checkInductiveness(dataset, type, mode):
    t = 'Inductive'
    f1 = open(dataset + '/fixedDS/'+t+'/'+type+'/'+mode+'.txt', 'r')
    all_lines = f1.readlines()
    print('total '+type +'_'+ mode + ' lines ' +str(len(all_lines)))
    all_lines = [line.split() for line in all_lines]
    for line in all_lines:
        if line[0] in train_entitites or line[2] in train_entitites:
            print(line)
    

#FB15 - 'Symmetry/People','inverse','AntiSymmetry', 'Inference'

types = ['Symmetry/People','inverse','AntiSymmetry', 'Inference']
dataset = 'fb15k'
for i in types:
    print(dataset +' - ' + i)
    readTrain(dataset, i)
    #WriteTransductive(dataset, i, 'valid')
    #WriteTransductive(dataset, i, 'test')
    #WriteInductive(dataset,i, 'valid')
    #WriteInductive(dataset,i, 'test')
    checkInductiveness(dataset, i , 'valid')
    checkInductiveness(dataset, i , 'test')
    #WriteSemiInductiveHeadTailBased(dataset,i , 'valid')
    #WriteSemiInductiveHeadTailBased(dataset,i , 'test')
    #WriteSemiInductiveCountBased(dataset,i, 'valid')
    #WriteSemiInductiveCountBased(dataset,i, 'test')
