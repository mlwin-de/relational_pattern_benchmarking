import numpy as np
import os
import argparse


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description='Generating graph features for datasets',
        usage='python  extract_graph_features.py --path <path to dataset folder>'
    )
    parser.add_argument('--path', default="../Datasets/", type=str, help='path to dataset folder')
    return parser.parse_args(args)


def check_inverse_relation_not_to_exist(train_data,test_data, input_directory,entity2id_inv, relation2id_inv ,dataset_name):
    print("------------------------+-----------------------")
    print("checking the triples for dataset inverse relations:", input_directory)


    
    train_dic = { (a, b,c):1 for a,b,c in train_data} #making it as h t r
    train_dic_out = { (a, b,c):1 for a,b,c in train_data} #making it as h t r
    train_dic_inv =  { (c, b, a):1 for a,b,c in train_data}  #making it as h t r
    test_dic = {(a, b,c):1 for a,b,c in test_data}
    test_dic_out = {(a, b,c):1 for a,b,c in test_data}
    test_dic_inv = {(c,b, a):1 for a,b,c in test_data}

    train = set(train_dic.keys())
    train_inv = set(train_dic_inv.keys())
    test = set(test_dic.keys())
    test_inv = set(test_dic_inv.keys())
    
    test_train_data_leak = False
    intesect0 = train.intersection(test)
    if len(intesect0) > 0:
        test_train_data_leak = True
        for a in intesect0:
            print("common triple:", (a[0],a[1],a[2])) 
            #del test_dic_out[(a[0],a[1],a[2])] #remove common triples from train instead of test.
            del train_dic_out[(a[0],a[1],a[2])]
    
    train_data = list(train_dic_out.keys())

    train_dic = { (a, b,c):1 for a,b,c in train_data} #making it as h t r
    train_dic_out = { (a, b,c):1 for a,b,c in train_data} #making it as h t r
    train_dic_inv =  { (c, b, a):1 for a,b,c in train_data}  #making it as h t r
    
    train = set(train_dic.keys())
    train_inv = set(train_dic_inv.keys())
    
    test_train_data_leak = False
    intesect0 = train.intersection(test)
    if len(intesect0) > 0:
        test_train_data_leak = True
        for a in intesect0:
            print("common triple:", (a[0],a[1],a[2])) 
            del test_dic_out[(a[0],a[1],a[2])]
    
    #keeping symm
    #intesect1= train.intersection(test_inv)
    #if len(intesect1) > 0:
    #    print ("between train and test symmetric_inverse relations exists: ")
    #    symmetric_inverse_existed = True
    #    for a in intesect1:
    #        #print ("in train and test symmetric_inverse relations exists: "+input_directory + dataset_name +": " +relation2id_inv.get(a[1],"NA") )
    #        print("in train: "+entity2id_inv.get(a[0]) +", " + relation2id_inv.get(a[1],"NA") + ", "+ entity2id_inv.get(a[2]))
    #        print("in test: "+entity2id_inv.get(a[2]) +", " + relation2id_inv.get(a[1],"NA") + ", "+ entity2id_inv.get(a[0] ))
    #        del test_dic_out[(a[2],a[1],a[0])]
    #        print ("")

    #print ("......")
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



    inverse_existed = False
    intersect2 = train_inv.intersection(test)
    if len(intersect2 )> 0:
        #print(intersect2)
        print ("between dataset train and test inverse relation exists:")
        inverse_existed = True
        for a in intersect2:
           #print ("in dataset train_inverse and test inverse relation exists: "+input_directory + ' '+ dataset_name +": " +relation2id_inv.get(train_dic_inv.get(a),"NA") +" "+relation2id_inv.get(test_dic.get(a),"NA"))
            if (relation2id_inv.get(train_dic_inv.get(a),"NA") != relation2id_inv.get(test_dic.get(a),"NA")): #already included in symmetry check
                print("in train: "+ entity2id_inv.get(a[1]) +", " + relation2id_inv.get(train_dic_inv.get(a),"NA") + ", "+ entity2id_inv.get(a[0]))
                print("in test: "+ entity2id_inv.get(a[0]) +", " + relation2id_inv.get(test_dic.get(a),"NA") + ", "+ entity2id_inv.get(a[1] ))
                #if test_dic_out.get( (test_dic.get(a)), None) is not None:
                del test_dic_out[(a[0],test_dic.get(a),a[1])]
                print ("")
            
    if test_train_data_leak:
        
        print("there is common triple between train and test in the dataset:"+ input_directory + dataset_name)
    else:
        print("there is no common triple between train and test in the dataset:"+ input_directory + dataset_name)
    if inverse_existed:
        data_leak = True
        print("there is common triple between train inv and test in the dataset:"+ input_directory + dataset_name)
    else:
        print("there is no common triple between train inv and test in the dataset:"+ input_directory + dataset_name)
    print ("-------------")
    
    return list(test_dic_out.keys()),train_data
    #train_dic = {}
    #test_dic = {}
    
    #train_dic = { (a, c):b for a,b,c in train_data}
    #train_dic_inv =  { (c, a):b for a,b,c in train_data}
    #test_dic = {(a, c):b for a,b,c in test_data}
    #test_dic_inv = {(c, a):b for a,b,c in test_data}

    #train = set(train_dic.keys())
    #train_inv = set(train_dic_inv.keys())
    #test = set(test_dic.keys())
    #test_inv = set(test_dic_inv.keys())

    ##intesect1= train.intersection(train_inv)
    ##if len(intesect1) > 0:
    ##    inverse_existed = True
    ##    for a in intesect1:
    ##        print ("in dataset train and traininverse inverse relations exists: "+input_directory+"/" + dataset_name +": " +relation2id_inv.get(train_dic.get(a),"NA")+" "+ relation2id_inv.get(train_dic_inv.get(a),"NA") )
    ##        print(entity2id_inv.get(a[0]) +", " + relation2id_inv.get(train_dic.get(a),"NA") + ", "+ entity2id_inv.get(a[1]))
    ##        print(entity2id_inv.get(a[1]) +", " + relation2id_inv.get(train_dic_inv.get(a),"NA") + ", "+ entity2id_inv.get(a[0] ))

    #intersect2 = train_inv.intersection(test)
    #if len(inverse_existed )> 0:
    #    for a in intersect2:
    #        print ("in dataset train_inverse and test  inverse relation exists: "+input_directory+"/" + dataset_name +": " +relation2id_inv.get(train_dic_inv.get(a),"NA") +" "+relation2id_inv.get(test_dic.get(a),"NA"))
    #        print(entity2id_inv.get(a[0]) +", " + relation2id_inv.get(train_dic_inv.get(a),"NA") + ", "+ entity2id_inv.get(a[1]))
    #        print(entity2id_inv.get(a[1]) +", " + relation2id_inv.get(test_dic.get(a),"NA") + ", "+ entity2id_inv.get(a[0] ))

    #if inverse_existed: 
    #    print("there is inverse relation in the dataset:"+ input_directory+"/" + dataset_name)
    #    print("")
        
    #    #np.save(input_directory + "/"+  dataset_name + "train_new.txx", train_data)
    #    #np.save(input_directory + "/"+  dataset_name + "test_new.txt", test_data)

    

def write_triple(file_path,triples, entity2id_inv, relation2id_inv):
    '''
    write triples and map them into ids.
    '''
    with open(file_path, "w") as fin:
        for line in triples:
            h, r, t = line
            fin.write(entity2id_inv[h] + '\t' + relation2id_inv[r] + '\t' + entity2id_inv[t] + '\n')


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

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

def check_train_test(args):
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
        #test_data_ = np.array(test_data_)[:, [0, 2, 1]]  # it's column must be in shape [entity, entity,relation]

        out_dir_path = input_directory +"/" +dataset_name #+ "/updated_dataset"
        #if os.path.isdir(out_dir_path):
        #    print("Directory %s to create already exists." % out_dir_path)
        #else:
        #    try:
        #        os.mkdir(out_dir_path)
        #    except OSError:
        #        print("Creation of the directory %s failed" % out_dir_path)
        #        exit()

        out_dir_path = out_dir_path + "/"
        test_out,train_out = check_inverse_relation_not_to_exist(train_data_, test_data_, out_dir_path,entity2id_inv, relation2id_inv, "")
           
        write_triple(out_dir_path+"cleaned_train.txt",train_out, entity2id_inv, relation2id_inv)
        write_triple(out_dir_path+"cleaned_test.txt",test_out, entity2id_inv, relation2id_inv)


print("example run: python check_data_leak_keep_sym.py --path ../Datasets/FB15K_H/Transductive")
check_train_test(parse_args())
# python check_data_leak_keep_sym.py --path ../Dataset/to_check