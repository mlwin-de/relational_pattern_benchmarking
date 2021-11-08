import numpy as np
import os
import argparse
#import torch

def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description='Generating graph features for datasets',
        usage='python  extract_graph_features.py --path <path to dataset folder>'
    )
    parser.add_argument('--type', default="inductive", type=str, help='dataset type: inductive, in_semi_htbased, in_semi_half')
    parser.add_argument('--path', default="../Datasets/", type=str, help='path to dataset folder')
    parser.add_argument('--path_original', default="../Datasets/Original_wn", type=str, help='path to original dataset folder')
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

#not complete. not using it.
def get_part_of_train_with_neghbors_of_valid_test(train_data_, test_data,valid_data_, out_dir_path,entity2id_inv, relation2id_inv,entity2id, relation2id, dataset_name):

    test_dic_entity = {}
    test_dic_relation = {}
    if len(valid_data_) != 0:
        test_data_ = test_data + valid_data_
    else:
        test_data_ = test_data


    for  i, triple in enumerate(test_data_):
        test_dic_entity[triple[0]] = 1
        test_dic_entity[triple[2]] = 1
        test_dic_relation[triple[1]] = 1

    #original_train = read_triple(out_dir_path + "/train_original.txt", entity2id, relation2id)


    train_dic_out = { (a, b,c):1 for a,b,c in train_data_} #making it as h t r
    #train = set(train_dic.keys())
    count = 0
    for i, triple in enumerate(train_data_):
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

def write_tain_test_inductive(original_data, file_path,triples_head_p, triples_tail_p, entity2id_inv, relation2id_inv,entity2id, relation2id):
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
    #size_limit_test = 2250 #to be reduced.
    #if len(triples_tail_p)> size_limit_test:
    #    #indices = torch.randperm(len(triples_tail_p))[:size_limit]
    #    indices = np.random.choice(len(triples_tail_p), size_limit_test)
    #    triples_tail_p = np.array(triples_tail_p)[indices.astype(int)]
    #    triples_tail_p = list(map(tuple, triples_tail_p))
    

    #if len(triples_head_p)> 10000:
    #    triples_head_p =shrink_train_to_neghbors_in_valid_test(triples_head_p, triples_tail_p_copy,valid_data_, file_path,entity2id_inv, relation2id_inv, "")

    #if len(triples_head_p)< 1000:
    #    triples_head_p =increase_train_with_more_neghbors_of_not_valid_test(triples_head_p, triples_tail_p_copy,valid_data_, file_path,entity2id_inv, relation2id_inv,entity2id, relation2id, "")
    


    #an idea to keep some triples to train the model! no. we make it fully inductive.
    #keep 1/3 of tails seperated so that the model knows how the pattern is, to add it to train. also keep the related head triples seperated in head triples and do not apply the cuts in this part. 
    # if randomly:
    #indices = np.random.choice(len(triples_tail_p), int(len(triples_tail_p)/ 3),  replace=False)
    #triples_tail_p_seperated_array = np.array(triples_tail_p)[indices.astype(int)]
    #triples_tail_p_seperated = list(map(tuple, triples_tail_p_seperated_array))
    #seperate the rest of test: 
    #triples_tail_p_dic =  { (a, b,c):1 for a,b,c in triples_tail_p}
    #for triple in triples_tail_p_seperated:
    #    del triples_tail_p_dic[triple]
    #triples_tail_p = list(triples_tail_p_dic.keys())
    triples_tail_p_seperated = triples_tail_p[0:int(len(triples_tail_p)/ 2)]
    triples_tail_p = triples_tail_p[int(len(triples_tail_p)/ 2):]
    triples_tail_p_dic = { (a, b,c):1 for a,b,c in triples_tail_p}

    triples_head_p = triples_head_p + triples_tail_p_seperated
    #related_head_triples_seperated = get_part_of_train_with_neghbors_of_valid_test(triples_head_p, triples_tail_p_copy,valid_data_, file_path,entity2id_inv, relation2id_inv,entity2id, relation2id, "")
    
    triples_head_p_copy = triples_head_p.copy()
    triples_tail_p_copy = triples_tail_p.copy()
    triples_head_p_dic =  { (a, b,c):1 for a,b,c in triples_head_p}
    triples_head_p_dic_out = triples_head_p_dic.copy()

    test_entities = {}
    for triple in triples_tail_p:
        test_entities[triple[0]] =1
        test_entities[triple[2]] =1

    valid_data_ = []

    #replace nodes.
    #when I remove an entity from train, I add another triple with
    #a) (for fully indutive) : remaining relation and two new entities ( must check if already not existing in both train and test)
    #b)  (for half inductive : head-tail based): remaining relation and one new entity( must check if already not existing in both train and test)
    #c) for count based incutive: half inductive hald transductive. : keep count of nodes. do the task of inductive for half of nodes in all the test set. 

    #case a
    all_triples_including_entity_as_h = {}
    for a,r,c in original_data:
        if all_triples_including_entity_as_h.get(a, None) is None:
                all_triples_including_entity_as_h[a] = [(a,r,c)]
        else:
            r_list = all_triples_including_entity_as_h[a]
            r_list.append((a,r,c))
            all_triples_including_entity_as_h[a] = r_list
    all_triples_including_entity_as_t = {}
    for a,r,c in original_data:        
        if all_triples_including_entity_as_t.get(c, None) is None:
                all_triples_including_entity_as_t[c] = [(a,r,c)]
        else:
            r_list = all_triples_including_entity_as_t[c]
            r_list.append((a,r,c))
            all_triples_including_entity_as_t[c] = r_list


    all_head_triples_including_entity_as_h = {}
    for a,r,c in triples_head_p:
        if all_head_triples_including_entity_as_h.get(a, None) is None:
                all_head_triples_including_entity_as_h[a] = [(a,r,c)]
        else:
            r_list = all_head_triples_including_entity_as_h[a]
            r_list.append((a,r,c))
            all_head_triples_including_entity_as_h[a] = r_list
    
    all_head_triples_including_entity_as_t = {}  
    for a,r,c in triples_head_p:     
        if all_head_triples_including_entity_as_t.get(c, None) is None:
                all_head_triples_including_entity_as_t[c] = [(a,r,c)]
        else:
            r_list = all_head_triples_including_entity_as_t[c]
            r_list.append((a,r,c))
            all_head_triples_including_entity_as_t[c] = r_list

    all_head_triples_including_entity = {}
    for a,r,c in triples_head_p:
        if all_head_triples_including_entity.get(a, None) is None:
                all_head_triples_including_entity[a] = [(a,r,c)]
        else:
            r_list = all_head_triples_including_entity[a]
            r_list.append((a,r,c))
            all_head_triples_including_entity[a] = r_list 
        if all_head_triples_including_entity.get(c, None) is None:
                all_head_triples_including_entity[c] = [(a,r,c)]
        else:
            r_list = all_head_triples_including_entity[c]
            r_list.append((a,r,c))
            all_head_triples_including_entity[c] = r_list

    all_triples_including_relation = {}
    for a,r,c in original_data:
        if all_triples_including_relation.get(r, None) is None:
                all_triples_including_relation[r] = [(a,r,c)]
        else:
            r_list = all_triples_including_relation[r]
            r_list.append((a,r,c))
            all_triples_including_relation[r] = r_list 
     

    for line in triples_tail_p:
        h, r, t = line
        #remove all triples including h and r from head_relations
        #replace them with triples from original that have the same relations in the removing triples.  
        #while replacing check that, also their entity do not exist in the tail_triples.
        #make this replacement one to one.

        h_triples_in_head_p_triples = all_head_triples_including_entity[h]
        t_triples_in_head_p_triples = all_head_triples_including_entity[t]
        #for triples containing h of test triple
        for triple in h_triples_in_head_p_triples:
            #remove
            if triples_head_p_dic_out.get(triple, None) is not None:
                del triples_head_p_dic_out[triple]
                #add replacement
                r_of_removed = triple[1]
                new_h_replacements = all_triples_including_relation[r_of_removed]
                count = 0
                for tr2 in new_h_replacements:
                    #head and trail are not in test and triple is not aleady in train
                    if test_entities.get(tr2[0], None) is None and test_entities.get(tr2[2], None) is None and triples_head_p_dic_out.get(tr2,None) is None and triples_tail_p_dic.get(tr2,None) is None and tr2 != triple:
                        replacement = tr2
                        triples_head_p_dic_out[replacement] = 1
                        #break #FIXME:is one enough? what if that h position is important. what if the replaced r has not any related triple in dataset
                        #replace with 2 triples. still ther is no gaurantee that we are bringing the pattern here.
                        #print("found!")
                        count = count + 1
                        if count == 2:
                            break
                #if count == 0:
                #    print("found none!")
        #now for t
        for triple in t_triples_in_head_p_triples:
            #remove
            if triples_head_p_dic_out.get(triple, None) is not None:
                del triples_head_p_dic_out[triple]
                #add replacement
                r_of_removed = triple[1]
                new_t_replacements = all_triples_including_relation[r_of_removed]
                count = 0
                for tr2 in new_t_replacements:
                    #head and trail are not in test and triple is not aleady in train
                    if test_entities.get(tr2[0], None) is None and test_entities.get(tr2[2], None) is None and triples_head_p_dic_out.get(tr2,None) is None and triples_tail_p_dic.get(tr2,None) is None and tr2 != triple:
                        replacement = tr2
                        triples_head_p_dic_out[replacement] = 1
                        #break
                        #print("found 2!")
                        count = count + 1
                        if count == 2:
                            break
                #if count == 0:
                #    print("found none 2!")
        
    triples_tail_p = list(triples_tail_p_dic.keys())
    triples_head_p = list(triples_head_p_dic_out.keys())
    counter = 1
    with open(file_path+"/inductive_train.txt", "w") as fin:
        for line in triples_head_p:
            h, r, t = line
            #triples.append(entity2id_inv[h], relation2id_inv[r], entity2id_inv[t])
            if triples_tail_p_dic.get(line,None) is None:
                fin.write(entity2id_inv[h] + '\t' + relation2id_inv[r] + '\t' + entity2id_inv[t] + '\n')
        with open(file_path+"/inductive_test.txt", "w") as fin2:
            with open(file_path+"/inductive_valid.txt", "w") as fin3:
                counter = 1
                for line in triples_tail_p:
                    h, r, t = line
                    if counter % 2 == 0:
                        fin2.write(entity2id_inv[h] + '\t' + relation2id_inv[r] + '\t' + entity2id_inv[t] + '\n')
                    else:
                        fin3.write(entity2id_inv[h] + '\t' + relation2id_inv[r] + '\t' + entity2id_inv[t] + '\n')
                    
                    counter = counter + 1
                


def write_tain_test_head_tail_based_semi_inductive(original_data, file_path,triples_head_p, triples_tail_p, entity2id_inv, relation2id_inv,entity2id, relation2id):
    '''
    write triples and map them into ids.
    all the head_p go to train
    in each 3 triples in tail_p one goes to test and 2 to train
    set an upper limit of 15000 triples before making test and train.
    '''

    triples_tail_p_seperated = triples_tail_p[0:int(len(triples_tail_p)/ 2)]
    triples_tail_p = triples_tail_p[int(len(triples_tail_p)/ 2):]
    triples_tail_p_dic = { (a, b,c):1 for a,b,c in triples_tail_p}

    triples_head_p = triples_head_p + triples_tail_p_seperated
    #related_head_triples_seperated = get_part_of_train_with_neghbors_of_valid_test(triples_head_p, triples_tail_p_copy,valid_data_, file_path,entity2id_inv, relation2id_inv,entity2id, relation2id, "")
    
    triples_head_p_copy = triples_head_p.copy()
    triples_tail_p_copy = triples_tail_p.copy()
    triples_head_p_dic =  { (a, b,c):1 for a,b,c in triples_head_p}
    triples_head_p_dic_out = triples_head_p_dic.copy()

    test_entities = {}
    for triple in triples_tail_p:
        test_entities[triple[0]] =1
        test_entities[triple[2]] =1

    valid_data_ = []

    #replace nodes.
    #when I remove an entity from train, I add another triple with
    #a) (for fully indutive) : remaining relation and two new entities ( must check if already not existing in both train and test)
    #b)  (for head tail half inductive : head-tail based): remaining relation and one new entity( must check if already not existing in both train and test)
    #c) for count based incutive: half inductive hald transductive. : keep count of nodes. do the task of inductive for half of nodes in all the test set. 

    #case b
    all_head_triples_including_entity = {}
    for a,r,c in triples_head_p:
        if all_head_triples_including_entity.get(a, None) is None:
                all_head_triples_including_entity[a] = [(a,r,c)]
        else:
            r_list = all_head_triples_including_entity[a]
            r_list.append((a,r,c))
            all_head_triples_including_entity[a] = r_list 
        if all_head_triples_including_entity.get(c, None) is None:
                all_head_triples_including_entity[c] = [(a,r,c)]
        else:
            r_list = all_head_triples_including_entity[c]
            r_list.append((a,r,c))
            all_head_triples_including_entity[c] = r_list

    all_tail_triples_including_entity = {}
    for a,r,c in triples_tail_p:
        if all_tail_triples_including_entity.get(a, None) is None:
                all_tail_triples_including_entity[a] = [(a,r,c)]
        else:
            r_list = all_tail_triples_including_entity[a]
            r_list.append((a,r,c))
            all_tail_triples_including_entity[a] = r_list 
        if all_tail_triples_including_entity.get(c, None) is None:
                all_tail_triples_including_entity[c] = [(a,r,c)]
        else:
            r_list = all_tail_triples_including_entity[c]
            r_list.append((a,r,c))
            all_tail_triples_including_entity[c] = r_list

    all_triples_including_relation = {}
    for a,r,c in original_data:
        if all_triples_including_relation.get(r, None) is None:
                all_triples_including_relation[r] = [(a,r,c)]
        else:
            r_list = all_triples_including_relation[r]
            r_list.append((a,r,c))
            all_triples_including_relation[r] = r_list 

    all_triples_including_h_r = {}
    for h,r,t in original_data:
        if all_triples_including_h_r.get((h,r), None) is None:
                all_triples_including_h_r[(h,r)] = [(h,r,t)]
        else:
            r_list = all_triples_including_h_r[(h,r)]
            r_list.append((h,r,t))
            all_triples_including_h_r[(h,r)] = r_list 
    all_triples_including_r_t = {}
    for h,r,t in original_data:
        if all_triples_including_r_t.get((r,t), None) is None:
                all_triples_including_r_t[(r,t)] = [(h,r,t)]
        else:
            r_list = all_triples_including_r_t[(r,t)]
            r_list.append((h,r,t))
            all_triples_including_r_t[(r,t)] = r_list 


    triples_tail_p_dic_copy = { (a, b,c):1 for a,b,c in triples_tail_p}
    for line in triples_tail_p:
        #remove all triples including h or t from head_relations
        #replace them with triples from original that have the same relations and non replacing entity in the removing triples.  
        #while replacing check that, also their entity do not exist in the tail_triples.
        #make this replacement one to one. or two to one
        #after replacing this entity, remove the triples from test to consider again because one entity of them is already replaced.
        if triples_tail_p_dic_copy.get(line,None) is None:
            continue
        h, r, t = line
        h_triples_in_head_p_triples = all_head_triples_including_entity[h]
        t_triples_in_head_p_triples = all_head_triples_including_entity[t]
        coin = np.random.randint(low=0, high=2, size=(1,))[0]
        #print(coin)
        if coin  == 1:
            #for triples containing h of test triple, remove all its occerances in train
            for triple in h_triples_in_head_p_triples:
                #remove
                if triples_head_p_dic_out.get(triple, None) is not None:
                    del triples_head_p_dic_out[triple]
                    #add replacement: triples from original that have the same relations and non replacing entity in the removing triples. (if head and tail are not same both r and t, but if both replace both with some triple that has that r)
                    replacement_found = False
                    r_of_removed = triple[1]
                    if h != t:
                        t_of_removed = triple[2]
                        new_h_replacements = all_triples_including_r_t[r_of_removed, t_of_removed]
                        for tr2 in new_h_replacements:
                            #head is not in test and triple is not aleady in train
                            if test_entities.get(tr2[0], None) is None and triples_head_p_dic_out.get(tr2,None) is None and triples_tail_p_dic.get(tr2,None) is None and tr2 != triple:
                                replacement = tr2
                                triples_head_p_dic_out[replacement] = 1
                                replacement_found = True
                                break 
                            #else: what if there is no replacement? then the test triple becomes fully inductive! to avoid it remove the triple from test too, or if h,t are the same replace with one triple having similar relation.

                    if h == t or replacement_found == False: # h == t
                        new_h_replacements = all_triples_including_relation[r_of_removed]
                        count = 0
                        for tr2 in new_h_replacements:
                            #trail is not in test and triple is not aleady in train
                            if test_entities.get(tr2[0], None) is None and test_entities.get(tr2[2], None) is None and triples_head_p_dic_out.get(tr2,None) is None and triples_tail_p_dic.get(tr2,None) is None and tr2 != triple:
                                replacement = tr2
                                triples_head_p_dic_out[replacement] = 1
                                replacement_found = True
                                break 
                            
                #if replacement_found == True: #remove the keeping entity from considering in future iterations.
                    if all_tail_triples_including_entity.get(h,None) is not None:
                        for triple2 in all_tail_triples_including_entity[h]:
                            if triples_tail_p_dic_copy.get(triple2,None) is not None:
                                del triples_tail_p_dic_copy[triple2]
                #else:#replacement not found. remove the triple from test to avoid becoming fully inductive
                #    del triples_tail_p_dic[triple]
                                
        else:
            #now for t
            for triple in t_triples_in_head_p_triples:
                #remove
                if triples_head_p_dic_out.get(triple, None) is not None:
                    del triples_head_p_dic_out[triple]
                    replacement_found = False
                    #add replacement
                    r_of_removed = triple[1]
                
                    if h != t:
                        h_of_removed = triple[0]
                        new_t_replacements = all_triples_including_h_r[h_of_removed, r_of_removed]
                        for tr2 in new_t_replacements:
                            #head and trail are not in test and triple is not aleady in train
                            if test_entities.get(tr2[2], None) is None and triples_head_p_dic_out.get(tr2,None) is None and triples_tail_p_dic.get(tr2,None) is None and tr2 != triple:
                                replacement = tr2
                                triples_head_p_dic_out[replacement] = 1
                                replacement_found = True
                                break
                    if h == t or replacement_found == False:
                        new_t_replacements = all_triples_including_relation[r_of_removed]
                        count = 0
                        for tr2 in new_t_replacements:
                            #head and trail are not in test and triple is not aleady in train
                            if test_entities.get(tr2[0], None) is None and test_entities.get(tr2[2], None) is None and triples_head_p_dic_out.get(tr2,None) is None and triples_tail_p_dic.get(tr2,None) is None and tr2 != triple:
                                replacement = tr2
                                triples_head_p_dic_out[replacement] = 1
                                replacement_found = True
                                break

                #if replacement_found == True: #remove the keeping entity from considering in future iterations.
                    if all_tail_triples_including_entity.get(t,None) is not None:
                        for triple2 in all_tail_triples_including_entity[t]:
                            if triples_tail_p_dic_copy.get(triple2,None) is not None:
                                del triples_tail_p_dic_copy[triple2]
                #else:#replacement not found. remove the triple from test to avoid becoming fully inductive
                #    del triples_tail_p_dic[triple]
            
        
    triples_tail_p = list(triples_tail_p_dic.keys())
    triples_head_p = list(triples_head_p_dic_out.keys())
    #now check from tails if both are not existing in the train remove it from tails:
    all_head_triples_including_entity = {}
    for a,r,c in triples_head_p:
        if all_head_triples_including_entity.get(a, None) is None:
                all_head_triples_including_entity[a] = [(a,r,c)]
        else:
            r_list = all_head_triples_including_entity[a]
            r_list.append((a,r,c))
            all_head_triples_including_entity[a] = r_list 
        if all_head_triples_including_entity.get(c, None) is None:
                all_head_triples_including_entity[c] = [(a,r,c)]
        else:
            r_list = all_head_triples_including_entity[c]
            r_list.append((a,r,c))
            all_head_triples_including_entity[c] = r_list
    
    triples_tail_p_dic = { (a, b,c):1 for a,b,c in triples_tail_p}

    for triple in triples_tail_p:
        if all_head_triples_including_entity.get(triple[0],None) is None and all_head_triples_including_entity.get(triple[2],None) is None:
            del triples_tail_p_dic[triple]
    triples_tail_p = list(triples_tail_p_dic.keys())

    counter = 1
    with open(file_path+"/ht_semi_inductive_train.txt", "w") as fin:
        for line in triples_head_p:
            h, r, t = line
            #triples.append(entity2id_inv[h], relation2id_inv[r], entity2id_inv[t])
            if triples_tail_p_dic.get(line,None) is None:
                fin.write(entity2id_inv[h] + '\t' + relation2id_inv[r] + '\t' + entity2id_inv[t] + '\n')
        with open(file_path+"/ht_semi_inductive_test.txt", "w") as fin2:
            with open(file_path+"/ht_semi_inductive_valid.txt", "w") as fin3:
                counter = 1
                for line in triples_tail_p:
                    h, r, t = line
                    if counter % 2 == 0:
                        fin2.write(entity2id_inv[h] + '\t' + relation2id_inv[r] + '\t' + entity2id_inv[t] + '\n')
                    else:
                        fin3.write(entity2id_inv[h] + '\t' + relation2id_inv[r] + '\t' + entity2id_inv[t] + '\n')
                    
                    counter = counter + 1
                

def write_tain_test_count_based_semi_inductive_half(original_data, file_path,triples_head_p, triples_tail_p, entity2id_inv, relation2id_inv,entity2id, relation2id):
    '''
    write triples and map them into ids.
    all the head_p go to train
    in each 3 triples in tail_p one goes to test and 2 to train
    set an upper limit of 15000 triples before making test and train.
    '''

    triples_tail_p_seperated = triples_tail_p[0:int(len(triples_tail_p)/ 2)]
    triples_tail_p = triples_tail_p[int(len(triples_tail_p)/ 2):]
    triples_tail_p_dic = { (a, b,c):1 for a,b,c in triples_tail_p}
    half_test_triple_num = int(len(triples_tail_p_dic)/2)
    triples_head_p = triples_head_p + triples_tail_p_seperated
    #related_head_triples_seperated = get_part_of_train_with_neghbors_of_valid_test(triples_head_p, triples_tail_p_copy,valid_data_, file_path,entity2id_inv, relation2id_inv,entity2id, relation2id, "")
    
    triples_head_p_copy = triples_head_p.copy()
    triples_tail_p_copy = triples_tail_p.copy()
    triples_head_p_dic =  { (a, b,c):1 for a,b,c in triples_head_p}
    triples_head_p_dic_out = triples_head_p_dic.copy()

    test_entities = {}
    for triple in triples_tail_p:
        test_entities[triple[0]] =1
        test_entities[triple[2]] =1

    valid_data_ = []

    #replace nodes.
    #when I remove an entity from train, I add another triple with
    #a) (for fully indutive) : remaining relation and two new entities ( must check if already not existing in both train and test)
    #b)  (for half inductive : head-tail based): remaining relation and one new entity( must check if already not existing in both train and test)
    #c) for count based incutive: half inductive hald transductive. : keep count of nodes. do the task of inductive for half of nodes in all the test set. 

    #case c
    all_triples_including_entity_as_h = {}
    for a,r,c in original_data:
        if all_triples_including_entity_as_h.get(a, None) is None:
                all_triples_including_entity_as_h[a] = [(a,r,c)]
        else:
            r_list = all_triples_including_entity_as_h[a]
            r_list.append((a,r,c))
            all_triples_including_entity_as_h[a] = r_list
    all_triples_including_entity_as_t = {}
    for a,r,c in original_data:        
        if all_triples_including_entity_as_t.get(c, None) is None:
                all_triples_including_entity_as_t[c] = [(a,r,c)]
        else:
            r_list = all_triples_including_entity_as_t[c]
            r_list.append((a,r,c))
            all_triples_including_entity_as_t[c] = r_list


    all_head_triples_including_entity_as_h = {}
    for a,r,c in triples_head_p:
        if all_head_triples_including_entity_as_h.get(a, None) is None:
                all_head_triples_including_entity_as_h[a] = [(a,r,c)]
        else:
            r_list = all_head_triples_including_entity_as_h[a]
            r_list.append((a,r,c))
            all_head_triples_including_entity_as_h[a] = r_list
    
    all_head_triples_including_entity_as_t = {}  
    for a,r,c in triples_head_p:     
        if all_head_triples_including_entity_as_t.get(c, None) is None:
                all_head_triples_including_entity_as_t[c] = [(a,r,c)]
        else:
            r_list = all_head_triples_including_entity_as_t[c]
            r_list.append((a,r,c))
            all_head_triples_including_entity_as_t[c] = r_list

    all_head_triples_including_entity = {}
    for a,r,c in triples_head_p:
        if all_head_triples_including_entity.get(a, None) is None:
                all_head_triples_including_entity[a] = [(a,r,c)]
        else:
            r_list = all_head_triples_including_entity[a]
            r_list.append((a,r,c))
            all_head_triples_including_entity[a] = r_list 
        if all_head_triples_including_entity.get(c, None) is None:
                all_head_triples_including_entity[c] = [(a,r,c)]
        else:
            r_list = all_head_triples_including_entity[c]
            r_list.append((a,r,c))
            all_head_triples_including_entity[c] = r_list

    all_triples_including_relation = {}
    for a,r,c in original_data:
        if all_triples_including_relation.get(r, None) is None:
                all_triples_including_relation[r] = [(a,r,c)]
        else:
            r_list = all_triples_including_relation[r]
            r_list.append((a,r,c))
            all_triples_including_relation[r] = r_list 
     
    
    triples_tail_p_out_dic_part1 = {}
    triples_tail_p_out_dic_part2 = {}
    main_counter_tails = 0
    for line in triples_tail_p:
        if main_counter_tails < half_test_triple_num:

        
            main_counter_tails = main_counter_tails + 1
            #print(main_counter_tails)
            h, r, t = line
            #remove all triples including h and r from head_relations
            #replace them with triples from original that have the same relations in the removing triples.  
            #while replacing check that, also their entity do not exist in the tail_triples.
            #make this replacement one to one.

            h_triples_in_head_p_triples = all_head_triples_including_entity[h]
            t_triples_in_head_p_triples = all_head_triples_including_entity[t]
            #for triples containing h of test triple
            for triple in h_triples_in_head_p_triples:
                #remove
                if triples_head_p_dic_out.get(triple, None) is not None:
                    del triples_head_p_dic_out[triple]
                    #add replacement
                    r_of_removed = triple[1]
                    new_h_replacements = all_triples_including_relation[r_of_removed]
                    count = 0
                    for tr2 in new_h_replacements:
                        #head and trail are not in test and triple is not aleady in train
                        if test_entities.get(tr2[0], None) is None and test_entities.get(tr2[2], None) is None and triples_head_p_dic_out.get(tr2,None) is None and triples_tail_p_dic.get(tr2,None) is None and tr2 != triple:
                            replacement = tr2
                            triples_head_p_dic_out[replacement] = 1
                            #break #FIXME:is one enough? what if that h position is important. what if the replaced r has not any related triple in dataset
                            #replace with 2 triples. still ther is no gaurantee that we are bringing the pattern here.
                            #print("found!")
                            count = count + 1
                            if count == 2:
                                break
                    #if count == 0:
                    #    print("found none!")
            #now for t
            for triple in t_triples_in_head_p_triples:
                #remove
                if triples_head_p_dic_out.get(triple, None) is not None:
                    del triples_head_p_dic_out[triple]
                    #add replacement
                    r_of_removed = triple[1]
                    new_t_replacements = all_triples_including_relation[r_of_removed]
                    count = 0
                    for tr2 in new_t_replacements:
                        #head and trail are not in test and triple is not aleady in train
                        if test_entities.get(tr2[0], None) is None and test_entities.get(tr2[2], None) is None and triples_head_p_dic_out.get(tr2,None) is None and triples_tail_p_dic.get(tr2,None) is None and tr2 != triple:
                            replacement = tr2
                            triples_head_p_dic_out[replacement] = 1
                            #break
                            #print("found 2!")
                            count = count + 1
                            if count == 2:
                                break
                    #if count == 0:
                    #    print("found none 2!"
            triples_tail_p_out_dic_part1[line] = 1
        else:#now for the rest check from tails if both are not existing in the train remove it from tails:
            
            if main_counter_tails == half_test_triple_num: #run this part only once

                #print(len(triples_tail_p_dic))   
                triples_head_p = list(triples_head_p_dic_out.keys())
                
                all_head_triples_including_entity = {}
                for a,r,c in triples_head_p:
                    if all_head_triples_including_entity.get(a, None) is None:
                        all_head_triples_including_entity[a] = [(a,r,c)]
                    else:
                        r_list = all_head_triples_including_entity[a]
                        r_list.append((a,r,c))
                        all_head_triples_including_entity[a] = r_list 
                    if all_head_triples_including_entity.get(c, None) is None:
                        all_head_triples_including_entity[c] = [(a,r,c)]
                    else:
                        r_list = all_head_triples_including_entity[c]
                        r_list.append((a,r,c))
                        all_head_triples_including_entity[c] = r_list
        

            #check if this part is fully existing.
            if all_head_triples_including_entity.get(line[0],None) is None and all_head_triples_including_entity.get(line[2],None) is None:
                triples_tail_p_out_dic_part1[line] = 1
                del triples_tail_p_dic[line]
            else:
                triples_tail_p_out_dic_part2[line] = 1
            #triples_tail_p = list(triples_tail_p_dic.keys())
            #print(half_test_triple_num, main_counter_tails)
            main_counter_tails = main_counter_tails + 1
    #now make the 50 percent count of inductive and transductive
    triples_tail_p_out_part1 = list(triples_tail_p_out_dic_part1.keys())
    triples_tail_p_out_part2 = list(triples_tail_p_out_dic_part2.keys())
    if (len(triples_tail_p_out_dic_part1) > len(triples_tail_p_out_dic_part2) ):
        diff = len(triples_tail_p_out_dic_part1) - len(triples_tail_p_out_dic_part2)
        triples_tail_p_out_part1 = triples_tail_p_out_part1[diff:]
    else:
        diff =  len(triples_tail_p_out_dic_part2) - len(triples_tail_p_out_dic_part1)
        triples_tail_p_out_part2 = triples_tail_p_out_part2[diff:]
    triples_tail_p = triples_tail_p_out_part1 + triples_tail_p_out_part2
    triples_head_p = list(triples_head_p_dic_out.keys())



    counter = 1
    with open(file_path+"/half_semi_inductive_train.txt", "w") as fin:
        for line in triples_head_p:
            h, r, t = line
            #triples.append(entity2id_inv[h], relation2id_inv[r], entity2id_inv[t])
            if triples_tail_p_dic.get(line,None) is None:
                fin.write(entity2id_inv[h] + '\t' + relation2id_inv[r] + '\t' + entity2id_inv[t] + '\n')
        with open(file_path+"/half_semi_inductive_test.txt", "w") as fin2:
            with open(file_path+"/half_semi_inductive_valid.txt", "w") as fin3:
                counter = 1
                for line in triples_tail_p:
                    h, r, t = line
                    if counter % 2 == 0:
                        fin2.write(entity2id_inv[h] + '\t' + relation2id_inv[r] + '\t' + entity2id_inv[t] + '\n')
                    else:
                        fin3.write(entity2id_inv[h] + '\t' + relation2id_inv[r] + '\t' + entity2id_inv[t] + '\n')
                    
                    counter = counter + 1
       

def make_train_test_db_from_pattern_db(args):
    input_directory = args.path
    input_directory_orginal = args.path_original
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

        head_data_ = read_triple(input_directory +"/"+  dataset_name + "/head_triples.txt", entity2id, relation2id)
 
        tail_data_ = read_triple(input_directory + "/"+ dataset_name + "/end_triples.txt", entity2id, relation2id)
        orginal_train =  read_triple(input_directory_orginal + "/" + "/train.txt", entity2id, relation2id) 
        orginal_test = read_triple(input_directory_orginal + "/" + "/test.txt", entity2id, relation2id) 
        orginal_valid = read_triple(input_directory_orginal + "/" + "/valid.txt", entity2id, relation2id) 
        original_data = orginal_train + orginal_test + orginal_valid
        out_dir_path = input_directory +"/" + dataset_name #+ "/updated_dataset"
        if args.type == "inductive":
            write_tain_test_inductive(original_data, out_dir_path,head_data_, tail_data_, entity2id_inv, relation2id_inv, entity2id, relation2id)
        if args.type == "ind_semi_htbased": 
            write_tain_test_head_tail_based_semi_inductive(original_data, out_dir_path,head_data_, tail_data_, entity2id_inv, relation2id_inv, entity2id, relation2id)
        if args.type == "ind_semi_half":
            write_tain_test_count_based_semi_inductive_half(original_data, out_dir_path,head_data_, tail_data_, entity2id_inv, relation2id_inv, entity2id, relation2id)

        print("done!")

       



#print("example run: python make_inductiveDBs.py --path ../Dataset/to_check --path_original ../Dataset/Original_wn/WN18 --type inductive")
make_train_test_db_from_pattern_db(parse_args())
# python make_inductiveDBs.py --path ../Dataset/to_check_wn --path_original ../Dataset/Original_wn/WN18 --type inductive  or ind_semi_half or nd_semi_htbased