import numpy as np
import os
import argparse


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description='Generating graph features for datasets',
        usage='python  extract_graph_features.py --path <path to dataset folder>'
    )
    parser.add_argument('--path', default="../Datasets/", type=str, help='path to dataset folder')
    parser.add_argument('--pattern', default="inference", type=str, help='selected pattern to extract')
    return parser.parse_args(args)

def read_triple(file_path, entity2id, relation2id):
    '''
    Read triples and map them into ids.
    '''
    triples = []
    with open(file_path) as fin:
        for line in fin:
            h, r, t = line.strip().split('\t')
            triples.append((entity2id[h], relation2id[r], entity2id[t]))
    return triples

def write_triple(file_path,triples, entity2id_inv, relation2id_inv):
    '''
    write triples and map them into ids.
    '''
    with open(file_path, "w") as fin:
        for line in triples:
            h, r, t = line
            #triples.append(entity2id_inv[h], relation2id_inv[r], entity2id_inv[t])
            fin.write(entity2id_inv[h] + '\t' + relation2id_inv[r] + '\t' + entity2id_inv[t] + '\n')

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

def extract_inference_pattern_v0(train_data,test_data, input_directory,entity2id_inv, relation2id_inv ,train_dic, train_dic_inv,test_dic_inv,train_dic_r,train_dic_r_inv,test_dic_r,test_dic_r_inv):
    print("------------------------+-----------------------")
    print("extracting triples for the dataset inference relations:", input_directory)
    inference_train = []
    inference_test = []
    dic_of_relations_with_inverse = {}
    #1. test relation if is in test triple list
    #2. test if the pattern is in train(so the model knows it) and if so:
    #3. search for the pattern in test and if so, extract it from train and test. the pattern must be between the train and test
    #4. test for not leaking from inverse relations
    for relation in relation2id_inv.keys():
        print("inspecting relation:" , relation)
        infereced_relation = []
        #1
        if test_dic_r.get(relation,None) is None:
                #print("relation is not in test")
                break

        #2
        pattern_exists_for_the_relation_in_train = False
        for triple_train in train_dic_r[relation]:
            f_e = triple_train[0]
            l_e = triple_train[2]
                
            #4.
            if train_dic_inv.get(triple_train, None) is not None:
                print("inverse triple_train exists for a triple, skipping to next relation.")
                dic_of_relations_with_inverse[relation] = 1
                break
            if test_dic_inv.get(triple_train, None) is not None:
                print("inverse triple exists for a triple, skipping to next relation.")
                dic_of_relations_with_inverse[relation] = 1
                break
            # (x,r1,y) -> (x,r2,y)
            kj = [x for x in train_data if (triple_train[1]== relation and x[0] == f_e and x[2] == l_e and not (triple_train[1] == x[1]))]
            if len (kj) > 0:
                #print (kj)
                pattern_exists_for_the_relation_in_train = True
                infereced_relation = kj[0][1]
                break

        #3
        if pattern_exists_for_the_relation_in_train:
            for triple in test_dic_r[relation]:
            
                 #4.
                if train_dic_inv.get(triple, None) is not None or dic_of_relations_with_inverse.get(relation, None) is not None :
                    print("inverse triple_train exists for a triple, skipping to next relation.")
                    dic_of_relations_with_inverse[relation] = 1
                    break
                if test_dic_inv.get(triple, None) is not None or dic_of_relations_with_inverse.get(relation, None)  is not None:
                    print("inverse triple exists for a triple, skipping to next relation.")
                    dic_of_relations_with_inverse[relation] = 1
                    break

                #if triple[1] == relation: 
                f_e = triple[0]
                l_e = triple[2]
                
                if train_dic_inv.get(triple, "NA") != "NA":
                    print("inverse triple exists for a triple, skipping to next relation.")
                    break
                # (x,r1,y) -> (x,r2,y)
                kj = [x for x in train_data if (triple[1]== relation and x[0] == f_e and x[2] == l_e and triple[1]== infereced_relation )]#not (triple[1] == x[1]))]
                # (x,r1, y) -> (y,r2,x) this is inverse, I am not including
                #kj2 = [x for x in train_data if (x[0] == l_e and x[2] == f_e and not (triple[1] == x[1]))]
                #there are many with more than one inverse form, just ignore
                if(len(kj) > 0): #if there is more than 1, it is maybe composition not inferference.
                    for a in kj:
                        print( "inference of relation from to: " + relation2id_inv[a[1]] + " ->" +relation2id_inv[triple[1]]  )
                        inference_test.append([f_e  + triple[1] , l_e ])
                        inference_train.append([a[0] ,  a[1] ,a[2]])
        
    return inference_test,inference_train


def merge_dics(dic1, dic2):
    merged = {}
    for key in dic1.keys():
        if key in dic2.keys():
            merged[key] = [*dic1[key], *dic2[key]]
        else:
            merged[key] = dic1[key]
    for key2 in dic2.keys():
        if key not in dic1.keys():
            merged[key] = dic2[key]
    return merged

#extraxted dataset in v0 is too small, extracting both train and test from train+test 
def extract_inference_pattern(train_data,test_data, input_directory,entity2id_inv, relation2id_inv ,train_dic, train_dic_inv,test_dic_inv,train_dic_r,train_dic_r_inv,test_dic_r,test_dic_r_inv):
    print("------------------------+-----------------------")
    print("extracting triples for the dataset inference relations:", input_directory)
    
    train_data = train_data  + test_data
    train_dic_inv = merge_dics(train_dic_inv , test_dic_inv)
    train_dic_r = merge_dics(train_dic_r , test_dic_r) 

    inference_train = []
    inference_test = []
    dic_of_relations_with_inverse = {}
    inference_train_dic_inv = {}
    inference_test_dic_inv = {}
    #method 2: extracting both train and test from train+test 
    
    #2. test if the pattern is in train(so the model knows it) and if so:
    #3. search for the pattern in test and if so, extract it from train and test. the pattern must be between the train and test
    #4. test for not leaking from inverse relations
    for relation in relation2id_inv.keys():
        print("inspecting relation:" , relation)
        infereced_relation = []
        
        #2
        pattern_exists_for_the_relation_in_train = False
        for triple in train_dic_r[relation]:
            f_e = triple[0]
            l_e = triple[2]
                
            #4. this check is left after generation because we have not train and test yet.
            #if inference_test_dic_inv.get(triple_train, None) is not None:
            #    print("inverse triple_train exists for a triple, skipping to next relation.")
            #    dic_of_relations_with_inverse[relation] = 1
            #    break
            #if test_dic_inv.get(triple_train, None) is not None:
            #    print("inverse triple exists for a triple, skipping to next relation.")
            #    dic_of_relations_with_inverse[relation] = 1
            #    break
            # (x,r1,y) -> (x,r2,y)
            kj = [x for x in train_data if (triple[1]== relation and x[0] == f_e and x[2] == l_e and not (triple[1] == x[1]))]
            if len (kj) > 0:
                #print (kj)
                pattern_exists_for_the_relation_in_train = True
                infereced_relation = kj[0][1]
                
                #this check is left after generation because we have not train and test yet.
                #if train_dic_inv.get(triple, "NA") != "NA":
                #    print("inverse triple exists for a triple, skipping to next relation.")
                #    break
                # (x,r1,y) -> (x,r2,y)
                #kj = [x for x in train_data if (triple[1]== relation and x[0] == f_e and x[2] == l_e and triple[1]== infereced_relation )]#not (triple[1] == x[1]))]
                # (x,r1, y) -> (y,r2,x) this is inverse, I am not including
                #kj2 = [x for x in train_data if (x[0] == l_e and x[2] == f_e and not (triple[1] == x[1]))]
                #there are many with more than one inverse form, just ignore
                #if(len(kj) > 0): #if there is more than 1, it is maybe composition not inferference.
                 
                for a in kj:
                    print( "inference of relation from to: " + relation2id_inv[a[1]] + " ->" +relation2id_inv[triple[1]]  )
                    #4.
                    #FIXME:for wn18 the number of test and valid is very small. should remove this checked.and do them outside. otherwise remove the inverse from train instead of test!
                    if inference_train_dic_inv.get(a, None) is not None: #or dic_of_relations_with_inverse.get(a[1], None) is not None :
                        print("inverse triple_train exists for a triple, skipping to next relation.")
                        dic_of_relations_with_inverse[relation] = 1
                        break
                    if inference_test_dic_inv.get(a, None) is not None:# or dic_of_relations_with_inverse.get(relation, None)  is not None:
                        print("inverse triple exists for a triple, skipping to next relation.")
                        dic_of_relations_with_inverse[relation] = 1
                        break
                    if dic_of_relations_with_inverse.get(relation, None) is None:
                        inference_train.append([a[0] ,  a[1] ,a[2]])
                        inference_train_dic_inv[(a[2],a[1],a[0])] = 1

                if dic_of_relations_with_inverse.get(relation, None) is None:
                    print( "inference of relation from to: " + relation2id_inv[a[1]] + " ->" +relation2id_inv[triple[1]]  )
                    inference_test.append([f_e  , triple[1] , l_e ])
                    inference_train_dic_inv[(l_e,triple[1],f_e)] = 1

                          
    return inference_test,inference_train 

def extract_anti_symm_pattern(train_data,test_data, input_directory,entity2id_inv, relation2id_inv ,train_dic, test_dic, train_dic_inv,test_dic_inv,train_dic_r,train_dic_r_inv,test_dic_r,test_dic_r_inv):
    print("extracting triples for the dataset anti_symm relations:", input_directory)

    anti_symm_head = {}
    anti_symm_tail = {}
    train_data = train_data  + test_data
    train_dic_inv = merge_dics(train_dic_inv , test_dic_inv)
    train_dic_r = merge_dics(train_dic_r , test_dic_r)
    train_dic = merge_dics(train_dic, test_dic) 

    all_triples_including_entity = {}
    for a,r,c in train_data:
            if all_triples_including_entity.get(a, None) is None:
                 all_triples_including_entity[a] = [(a,r,c)]
            else:
                r_list = all_triples_including_entity[a]
                r_list.append((a,r,c))
                all_triples_including_entity[a] = r_list
            
            if all_triples_including_entity.get(c, None) is None:
                 all_triples_including_entity[c] = [(a,r,c)]
            else:
                r_list = all_triples_including_entity[c]
                r_list.append((a,r,c))
                all_triples_including_entity[c] = r_list



    for relation in relation2id_inv.keys():

        for triple_train in train_dic_r[relation]:
            a = triple_train[0]
            x = triple_train[2]
            for triple_train2 in train_dic_r[relation]:
                y = triple_train2[0]
                a2 = triple_train2[2]
                # (a,r,x) and (y,r,a) -> x!=y which means in test there is v and u such that (x,r,v) or (u,r,y). 
                if a == a2 and x != y and train_dic.get((a,relation,a),None) is None and train_dic.get((x,relation,x),None) is None and train_dic.get((y,relation,y),None) is None : #this is an unti
                    for triple_train3 in train_dic_r[relation]:
                        x3 = triple_train3[0]
                        v = triple_train3[2]
                        if x3 == x and v!= a:
                            anti_symm_head[(triple_train)] = 1
                            anti_symm_head[(triple_train2)] = 1
                            anti_symm_tail[(triple_train3)] = 1
                            #add one more triple including v
                            more_triples = all_triples_including_entity.get(v, None)
                            if more_triples is not None:
                                anti_symm_head[(more_triples[0])] = 1


            #todo : fix here
                #if a == a2 and x != y and train_dic.get((a,relation,a),None) is None and train_dic.get((x,relation,x),None) is None and train_dic.get((y,relation,y),None) is None : #this is an unti
                    #for triple_train3 in train_dic_r[relation]:
                        u = triple_train3[0]
                        y3 = triple_train3[2]
                        if y3 == y and u != a:
                            anti_symm_head[(triple_train)] = 1
                            anti_symm_head[(triple_train2)] = 1
                            anti_symm_tail[(triple_train3)] = 1
                            #add one more triple including u
                            more_triples = all_triples_including_entity.get(u, None)
                            if more_triples is not None:
                                anti_symm_head[(more_triples[0])] = 1

    return list(anti_symm_tail.keys()),list(anti_symm_head.keys())         

def extract_symm_pattern(train_data,test_data, input_directory,entity2id_inv, relation2id_inv ,dataset_name, train_dic, train_dic_inv):
    print("------------------------+-----------------------")
    print("extracting triples for the dataset symm relations:", input_directory)

    symm_train = []
    symm_test = []

    train_dic = { (a, b,c):1 for a,b,c in train_data} #making it as h t r
    train_dic_inv =  { (c, b, a):1 for a,b,c in train_data}  #making it as h t r
    test_dic = {(a, b,c):1 for a,b,c in test_data}
    test_dic_out = {(a, b,c):1 for a,b,c in test_data}
    test_dic_inv = {(c,b, a):1 for a,b,c in test_data}

    train = set(train_dic.keys())
    train_inv = set(train_dic_inv.keys())
    test = set(test_dic.keys())
    test_inv = set(test_dic_inv.keys())
    
    intesect1= train.intersection(test_inv)
    if len(intesect1) > 0:
        print ("between train and test symmetric_inverse relations exists: ")
        symmetric_inverse_existed = True
        for a in intesect1:
            #print ("in train and test symmetric_inverse relations exists: "+input_directory + dataset_name +": " +relation2id_inv.get(a[1],"NA") )
            print("in train: "+entity2id_inv.get(a[0]) +", " + relation2id_inv.get(a[1],"NA") + ", "+ entity2id_inv.get(a[2]))
            print("in test: "+entity2id_inv.get(a[2]) +", " + relation2id_inv.get(a[1],"NA") + ", "+ entity2id_inv.get(a[0] ))
            symm_train.append((a[0],a[1],a[2]))
            symm_test.append((a[2],a[1],a[0]))
            print ("")

    return symm_test, symm_train

def extract_inverse_pattern(train_data,test_data, input_directory,entity2id_inv, relation2id_inv ,dataset_name, train_dic, train_dic_inv):
    print("------------------------+-----------------------")
    print("extracting triples for the dataset inverse relations:", input_directory)

    #we have enough data in original WN18 and FB15k with this pattern that do not need to merge their train and test to exract new datasets. 
    #train_data=  train_data  + test_data
    #train_dic_inv = merge_dics(train_dic_inv , test_dic_inv)
    #train_dic_r = merge_dics(train_dic_r , test_dic_r) 



    train_dic = {}
    test_dic = {}
    
    train_dic = { (a, c):b for a,b,c in train_data}
    train_dic_inv =  { (c, a):b for a,b,c in train_data}
    test_dic = {(a, c):b for a,b,c in test_data}
    test_dic_inv = {(c, a):b for a,b,c in test_data}

    train = set(train_dic.keys())
    train_inv = set(train_dic_inv.keys())
    test = set(test_dic.keys())
    test_inv = set(test_dic_inv.keys())

    inverse_train = []
    inverse_test = []
    inverse_existed = False
    intersect2 = train_inv.intersection(test)
    if len(intersect2 )> 0:
        print ("between dataset train and test inverse relation exists:")
        for a in intersect2:
            if (relation2id_inv.get(train_dic_inv.get(a),"NA") != relation2id_inv.get(test_dic.get(a),"NA")): #already included in symmetry check, here only inverse
                print ("inverse relation : " +relation2id_inv.get(train_dic_inv.get(a),"NA") +" to "+relation2id_inv.get(test_dic.get(a),"NA"))
                #print("in train: "+ entity2id_inv.get(a[1]) +", " + relation2id_inv.get(train_dic_inv.get(a),"NA") + ", "+ entity2id_inv.get(a[0]))
                #print("in test: "+ entity2id_inv.get(a[0]) +", " + relation2id_inv.get(test_dic.get(a),"NA") + ", "+ entity2id_inv.get(a[1] ))
                inverse_train.append((a[1],train_dic_inv.get(a),a[0]))
                inverse_test.append((a[0],test_dic.get(a),a[1]))
                
            

    print ("-------------")

    return inverse_test, inverse_train
    

def extract_pattern(args):
    input_directory = args.path
    print("-------------------------------------------------------")
    print("testing dir: " + input_directory)
    filenames = listdir_nohidden(input_directory)  # get all files' and folders' names in the current directory, ignore hidder folders
    filenames = [_ for _ in filenames] 
    print("extracting entity features related to datasets:", filenames)
    
    #print("(please give folder of folders like ../data/ where ../data/WN18 is inside it)")
    result = []
    for filename in filenames:  # loop through all the files and folders
        if os.path.isdir(os.path.join(input_directory, filename)):  # check whether the current object is a folder
            result.append(filename)

    result.sort()

    for dataset_name in result:
        if not os.path.exists(input_directory + "/"+  dataset_name + '/entities.dict'):
            print("entities.dict does not exist. first run makedict_for_pattern_rel_dbs.py to generate that. folder: "+input_directory + "/"+  dataset_name )
            exit()

        with open(input_directory +"/"+  dataset_name + '/entities.dict') as fin:
            entity2id = dict()
            entity2id_inv = {}
            for line in fin:
                eid, entity = line.strip().split('\t')
                entity2id[entity] = int(eid)
                entity2id_inv[int(eid)]=entity

                

        with open(input_directory + "/"+ dataset_name + '/relations.dict') as fin:
            relation2id = {}
            relation2id_inv = {}
            for line in fin:
                rid, relation = line.strip().split('\t')
                relation2id[relation] = int(rid)
                relation2id_inv[int(rid)]=relation

        train_data_ = read_triple(input_directory +"/"+  dataset_name + "/train.txt", entity2id, relation2id)
        #train_data_ = np.array(train_data_)[:, [0, 2, 1]]  # it's column must be in shape [entity, entity,relation]

        test_data_ = read_triple(input_directory + "/"+ dataset_name + "/test.txt", entity2id, relation2id)
        #valid_data_ = read_triple(input_directory + "/"+ dataset_name + "/valid.txt", entity2id, relation2id)
        #test_data_ = (test_data_ + valid_data_)

        out_dir_path = input_directory +"/" +dataset_name #+ "/updated_dataset"

        train_dic = { (a, b,c):1 for a,b,c in train_data_} #making it as h t r
        train_dic_inv =  { (c, b, a):1 for a,b,c in train_data_}  #making it as h t r
        test_dic = {(a, b,c):1 for a,b,c in test_data_}
        test_dic_inv = {(c,b, a):1 for a,b,c in test_data_}

        train_dic_r = {}
        train_dic_r_inv = {}
        test_dic_r = {}
        test_dic_r_inv = {}
        for a,r,c in train_data_:
            if train_dic_r.get(r, None) is None:
                 train_dic_r[r] = [(a,r,c)]
            else:
                r_list = train_dic_r[r]
                r_list.append((a,r,c))
                train_dic_r[r] = r_list

        for a,r,c in train_data_:
            if train_dic_r_inv.get(r, None) is None:
                 train_dic_r_inv[r] = [(c,r,a)]
            else:
                r_list = train_dic_r_inv[r]
                r_list.append((c,r,a))
                train_dic_r_inv[r] = r_list
       

        for a,r,c in test_data_:
            if test_dic_r.get(r, None) is None:
                 test_dic_r[r] = [(a,r,c)]
            else:
                r_list = test_dic_r[r]
                r_list.append((a,r,c))
                test_dic_r[r] = r_list

        for a,r,c in test_data_:
            if test_dic_r_inv.get(r, None) is None:
                 test_dic_r_inv[r] = [(c,r,a)]
            else:
                r_list = test_dic_r_inv[r]
                r_list.append((c,r,a))
                test_dic_r_inv[r] = r_list
       

        out_dir_path = out_dir_path + "/"
    
        if args.pattern == "inference":
            inference_test,inference_train = extract_inference_pattern(train_data_, test_data_, out_dir_path,entity2id_inv, relation2id_inv, train_dic, train_dic_inv, test_dic_inv,train_dic_r,train_dic_r_inv,test_dic_r,test_dic_r_inv)
            train_file_path = out_dir_path + "inference_head_triples.txt" #they then get processed to make train and test
            test_file_path = out_dir_path + "inference_end_triples.txt"
            write_triple(train_file_path,inference_train, entity2id_inv, relation2id_inv)
            write_triple(test_file_path,inference_test, entity2id_inv, relation2id_inv)

        if args.pattern == "symm":
            symm_test , symm_train = extract_symm_pattern(train_data_, test_data_, out_dir_path,entity2id_inv, relation2id_inv, train_dic, train_dic_inv, test_dic_inv)
            train_file_path = out_dir_path + "symm_head_triples.txt"
            test_file_path = out_dir_path + "symm_end_triples.txt"
            write_triple(train_file_path,symm_train, entity2id_inv, relation2id_inv)
            write_triple(test_file_path,symm_test, entity2id_inv, relation2id_inv)

        
        if args.pattern == "antisymm": #not implemented. the code is copy from inference
            antisymm_test, antisymm_train =  extract_anti_symm_pattern(train_data_, test_data_, out_dir_path,entity2id_inv, relation2id_inv, train_dic,test_dic, train_dic_inv, test_dic_inv,train_dic_r,train_dic_r_inv,test_dic_r,test_dic_r_inv)
            train_file_path = out_dir_path + "anti_head_triples.txt"
            test_file_path = out_dir_path + "anti_end_triples.txt"
            write_triple(train_file_path,antisymm_train, entity2id_inv, relation2id_inv)
            write_triple(test_file_path,antisymm_test, entity2id_inv, relation2id_inv)

        if args.pattern == "inverse": 
            inverse_test, inverse_train = extract_inverse_pattern(train_data_,test_data_, out_dir_path,entity2id_inv, relation2id_inv ,dataset_name, train_dic, train_dic_inv)
            train_file_path = out_dir_path + "inverse_head_triples.txt"
            test_file_path = out_dir_path + "inverse_end_triples.txt"
            write_triple(train_file_path,inverse_train, entity2id_inv, relation2id_inv)
            write_triple(test_file_path,inverse_test, entity2id_inv, relation2id_inv)
        
        return

print("example run: python extract_pattern_dataset.py --path ../Dataset/Original/   --pattern inference") # symm antisymm
# python extract_pattern_dataset.py --path ../Dataset/WN18/ --pattern symm
# python extract_pattern_dataset.py --path ../Dataset/Original/ --pattern symm   
extract_pattern(parse_args())

# requires python 3.9
#source ~/miniconda3/bin/activate
#first screen for inference: 57 finished.
#next for symm
