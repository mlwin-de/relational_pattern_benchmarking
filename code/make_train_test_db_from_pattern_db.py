import numpy as np
import os
import argparse
#import torch

def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description='Generating graph features for datasets',
        usage='python  extract_graph_features.py --path <path to dataset folder>'
    )
    parser.add_argument('--path', default="../Datasets/", type=str, help='path to dataset folder')
    parser.add_argument('--pattern', default="inference", type=str, help='selected pattern to extract')
    return parser.parse_args(args)

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f


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

def get_stats(train_data, test_data,valid_data, input_directory,entity2id_inv, relation2id_inv, dataset_name):
    print("------------------------+-----------------------")
    print("finding dataset statistics: ", input_directory)
    
    valid_data_ = valid_data.copy()
    test_data_ = test_data.copy()
    train_data_ = train_data.copy()
    num_triples_train = len(train_data_)
    num_triples_test = len(test_data_)
    num_triples_valid = len(valid_data_)
    if num_triples_valid != 0:
        test_data_ =  test_data_  + valid_data_
    test_data_ = test_data_  + train_data_
    sum_ = test_data_

    sum_entity = {}
    sum_rel = {}
    for  i, triple in enumerate(sum_):
        sum_entity[triple[0]] = 1
        sum_entity[triple[2]] = 1
        sum_rel[triple[1]] = 1

    sum_entity_num = len(sum_entity.keys())


    #sum_entity_num =len({ {(a):1, (c):1 }for a,b,c in sum_})
    sum_rel_num = len(sum_rel.keys())
    print("num_triples_train: ", num_triples_train)
    print("num_triples_test:" , num_triples_test)
    print("num_triples_valid: ", num_triples_valid)
    print("total entity_num: ", sum_entity_num) 
    print("total rel_num: ", sum_rel_num)
  


def shrink_train_to_neghbors_in_valid_test(train_data_, test_data_,valid_data_, out_dir_path,entity2id_inv, relation2id_inv, dataset_name):
    print("------------------------+-----------------------")

    print("stats before shrink:")
    get_stats(train_data_, test_data_,valid_data_, out_dir_path,entity2id_inv, relation2id_inv, dataset_name)

    test_dic_entity = {}
    test_dic_relation = {}
    test_data_o = test_data_.copy()
    if len(valid_data_) != 0:
        test_data_ = test_data_ + valid_data_

    for  i, triple in enumerate(test_data_):
        test_dic_entity[triple[0]] = 1
        test_dic_entity[triple[2]] = 1
        test_dic_relation[triple[1]] = 1

    train_dic_out = { (a, b,c):1 for a,b,c in train_data_} #making it as h t r
    #train = set(train_dic.keys())
    count = 0
    for i, triple in enumerate(train_data_):
        if test_dic_entity.get( (triple[0]), None) is None and test_dic_entity.get( (triple[2]), None) is None :#and test_dic_relation.get( (triple[1]), None) is None
            #print("none of the head, tail and relaiton of the triple is in valid/test sets", triple)
            if train_dic_out.get(triple, None) is not None:
                count = count + 1
                del train_dic_out[triple]
        

    print ("number of removed:", count)
    
    train_data_ = list(train_dic_out.keys())
    print("stats increase shrink:")
    get_stats(train_data_, test_data_o,valid_data_, out_dir_path,entity2id_inv, relation2id_inv, dataset_name)
    return train_data_

def increase_train_with_more_neghbors_of_not_valid_test(train_data_, test_data_,valid_data_, out_dir_path,entity2id_inv, relation2id_inv,entity2id, relation2id, dataset_name):
    print("------------------------+-----------------------")

    print("stats before increase:")
    get_stats(train_data_, test_data_,valid_data_, out_dir_path,entity2id_inv, relation2id_inv, dataset_name)

    test_dic_entity = {}
    test_dic_relation = {}
    if len(valid_data_) != 0:
        test_data_ = test_data_ + valid_data_

    for  i, triple in enumerate(test_data_):
        test_dic_entity[triple[0]] = 1
        test_dic_entity[triple[2]] = 1
        test_dic_relation[triple[1]] = 1

    original_train = read_triple(out_dir_path + "/train_original.txt", entity2id, relation2id)


    train_dic_out = { (a, b,c):1 for a,b,c in train_data_} #making it as h t r
    #train = set(train_dic.keys())
    count = 0
    for i, triple in enumerate(original_train):
        if test_dic_entity.get( (triple[0]), None) is None and test_dic_entity.get( (triple[2]), None) is None  :
            #print("none of the head, tail and relaiton of the triple is in valid/test sets", triple)
            #if train_dic_out.get(triple, None) is not None:
            count = count + 1
            train_dic_out[triple] = 1
            if count == 1500:
                break

    print ("number of added triples:", count)
    
    train_data_ = list(train_dic_out.keys())
    print("stats after shrink:")
    get_stats(train_data_, test_data_,valid_data_, out_dir_path,entity2id_inv, relation2id_inv, dataset_name)
    return train_data_

def write_tain_test(file_path,triples_head_p, triples_tail_p, entity2id_inv, relation2id_inv,entity2id, relation2id):
    '''
    write triples and map them into ids.
    all the head_p go to train
    in each 3 triples in tail_p one goes to test and 2 to train
    set an upper limit of 15000 triples before making test and train.
    '''
    #size_limit_train = 10000
    #if len(triples_head_p)> size_limit:
    #    indices = np.random.choice(len(triples_head_p), size_limit_train)
    #    triples_head_p = np.array(triples_head_p)[indices.astype(int)]
    
    #instead sizelimit the test, because it is the test that train can be shrinkt opon.
    size_limit_test = 2250 #to be reduced.
    if len(triples_head_p)> size_limit_test:
        #indices = torch.randperm(len(triples_tail_p))[:size_limit]
        indices = np.random.choice(len(triples_tail_p), size_limit_test)
        triples_tail_p = np.array(triples_tail_p)[indices.astype(int)]
        triples_tail_p = list(map(tuple, triples_tail_p))
    
    triples_tail_p_copy = triples_tail_p.copy()
    valid_data_ = []
    if len(triples_head_p)> 10000:
        triples_head_p =shrink_train_to_neghbors_in_valid_test(triples_head_p, triples_tail_p_copy,valid_data_, file_path,entity2id_inv, relation2id_inv, "")

    if len(triples_head_p)< 1000:
        triples_head_p =increase_train_with_more_neghbors_of_not_valid_test(triples_head_p, triples_tail_p_copy,valid_data_, file_path,entity2id_inv, relation2id_inv,entity2id, relation2id, "")
    

    counter = 1
    with open(file_path+"/train.txt", "w") as fin:
        for line in triples_head_p:
            h, r, t = line
            #triples.append(entity2id_inv[h], relation2id_inv[r], entity2id_inv[t])
            fin.write(entity2id_inv[h] + '\t' + relation2id_inv[r] + '\t' + entity2id_inv[t] + '\n')
        with open(file_path+"/test.txt", "w") as fin2:
            with open(file_path+"/valid.txt", "w") as fin3:
                counter = 1
                for line in triples_tail_p:
                    h, r, t = line
                    if counter % 3 == 0:
                        fin2.write(entity2id_inv[h] + '\t' + relation2id_inv[r] + '\t' + entity2id_inv[t] + '\n')
                    elif counter % 3 == 1:
                        fin3.write(entity2id_inv[h] + '\t' + relation2id_inv[r] + '\t' + entity2id_inv[t] + '\n')
                    else:
                        fin.write(entity2id_inv[h] + '\t' + relation2id_inv[r] + '\t' + entity2id_inv[t] + '\n')
                    counter = counter + 1
                
    
def make_train_test_db_from_pattern_db(args):
    input_directory = args.path
    print("-------------------------------------------------------")
    print("working dir: " + input_directory)
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

        head_data_ = read_triple(input_directory +"/"+  dataset_name + "/head_triples.txt", entity2id, relation2id)
 
        tail_data_ = read_triple(input_directory + "/"+ dataset_name + "/end_triples.txt", entity2id, relation2id)

        out_dir_path = input_directory +"/" + dataset_name #+ "/updated_dataset"
        write_tain_test(out_dir_path,head_data_, tail_data_, entity2id_inv, relation2id_inv, entity2id, relation2id)
        print("done!")

       



print("example run: python make_train_test_db_from_pattern_db.py --path ../Dataset/WN18_N/")
make_train_test_db_from_pattern_db(parse_args())
# python make_train_test_db_from_pattern_db.py --path ../Dataset/to_check