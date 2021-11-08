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


def get_stats(train_data_, test_data_,valid_data_, input_directory,entity2id_inv, relation2id_inv, dataset_name):
    print("------------------------+-----------------------")
    print("finding dataset statistics: ", input_directory)

    num_triples_train = len(train_data_)
    num_triples_test = len(test_data_)
    num_triples_valid = len(valid_data_)

    #test_dic_entity = {(a):1,(c):1 for a,b,c in test_data}
    #test_dic_relation = {(b):1 for a,b,c in test_data}

    #valid_dic_entity = {(a):1,(c):1 for a,b,c in valid_data}
    #valid_dic_relation = {(b):1 for a,b,c in valid_data}

    #test_dic_entity = {(a):1,(c):1 for a,b,c in valid_data}
    #test_dic_relation = {(b):1 for a,b,c in valid_data}
    
    test_data_ = test_data_  + valid_data_
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

def read_and_run(args):
    input_directory = args.path
    print("-------------------------------------------------------")
    print("dir: " + input_directory)
    filenames = listdir_nohidden(input_directory)  # get all files' and folders' names in the current directory, ignore hidder folders
    filenames = [_ for _ in filenames] 
    
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

        valid_data_ = read_triple(input_directory + "/"+ dataset_name + "/valid.txt", entity2id, relation2id)
        
        test_data_ = read_triple(input_directory + "/"+ dataset_name + "/test.txt", entity2id, relation2id)
        
        out_dir_path = ""
        get_stats(train_data_, test_data_,valid_data_, dataset_name,entity2id_inv, relation2id_inv, "")
           


print("example run: python get_dataset_stats.py --path ../Datasets/FB15K_H/Transductive")
read_and_run(parse_args())
