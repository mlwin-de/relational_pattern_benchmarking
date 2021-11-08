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


def make_test_valid_files_half(original_data, file_path,entity2id_inv, relation2id_inv,entity2id, relation2id):
    '''
    throw out half size of valid and test files.

    '''
    counter = 1
    counter2 = 0 
    with open(file_path+"/new_test.txt", "w") as fin:
        with open(file_path+"/new_valid.txt", "w") as fin2:
            for line in original_data:
                counter = counter +1 
                if counter % 2 == 0:
                    h, r, t = line
                    counter2 = counter2 + 1
                    if counter2 % 2 == 0:
                        fin2.write(entity2id_inv[h] + '\t' + relation2id_inv[r] + '\t' + entity2id_inv[t] + '\n')
                    else:
                        fin.write(entity2id_inv[h] + '\t' + relation2id_inv[r] + '\t' + entity2id_inv[t] + '\n')
       
    print("done!")

def run(args):
    input_directory = args.path
    print("-------------------------------------------------------")
    print("working dir: " + input_directory)
    filenames = listdir_nohidden(input_directory)  # get all files' and folders' names in the current directory, ignore hidder folders
    filenames = [_ for _ in filenames] 
    print("making dataset of with inductive setting:", filenames)
    
    #print("(please give folder of folders like ../data/ where ../data/WN18 is inside it)")
    result = []
    for filename in filenames:  # loop through all the files and folders
        if os.path.isdir(os.path.join(input_directory, filename)):  # check whether the current object is a folder
            result.append(filename)

    result.sort()

    for dataset_name in result:
        print("processing ",dataset_name)
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


        test = read_triple(input_directory +  dataset_name+ "/test.txt", entity2id, relation2id) 
        valid = read_triple(input_directory +  dataset_name + "/valid.txt", entity2id, relation2id) 
        test = test + valid
        out_dir_path = input_directory +  dataset_name
        make_test_valid_files_half(test, out_dir_path, entity2id_inv, relation2id_inv, entity2id, relation2id)

        print("done!")

       



#print("example run: python make_test_valid_files_half.py --path ../Dataset/to_check ")
run(parse_args())
