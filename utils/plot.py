import numpy as np
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

sns.set(rc={'figure.figsize':(11.7,8.27)})
palette = sns.color_palette("bright", 10)
a = np.load("entity_embedding.npy")
f1 = open('../fb15k/fixedDS/Inductive/Symmetry/People/entities.dict', "r")
entity_emb_dict = {}
#loading embedding for each entity; dictionary is with key = Id of entity and Value = Embedding for this entity
i = 0
for l in a: 
    entity_emb_dict[i] = l
    i = i + 1

X = np.empty((2,1000), int)
f = open('../fb15k/fixedDS/Inductive/Symmetry/People/train2id.txt') 
for line in f.readlines():
    line = line.split()
    if len(line) > 1:
        #print(type(line))
        #head
        h = int(line[0])
        t = int(line[1])
        r = int(line[2])
        #take its embedding
        h_e = entity_emb_dict[h]
        t_e = entity_emb_dict[t]
        #n = np.concatenate((h_e, t_e), axis=0)        
        #concat the two entities
        n = np.vstack([h_e,t_e])
        #print(n.shape)
        #add to central array
        X = np.append(X, n, axis=0)
print(n.shape)
print(X.shape)
#for labeling - train has label 0
li = np.zeros(X.shape[0])
#for coloring - train has color blue
li_color = ['blue']*(X.shape[0])

#do the same for valid
X_valid = np.empty((2,1000), int)
f = open('../fb15k/fixedDS/Inductive/Symmetry/People/valid2id.txt') 
for line in f.readlines():
    line = line.split()
    if len(line) > 1:
        #print(type(line))
        #head
        h = int(line[0])
        t = int(line[1])
        r = int(line[2])
        h_e = entity_emb_dict[h]
        t_e = entity_emb_dict[t]
        #n = np.concatenate((h_e, t_e), axis=0)        
        n = np.vstack([h_e,t_e])
        #print(n.shape)
        X_valid = np.append(X_valid, n, axis=0)
print(n.shape)
print(X_valid.shape)
#X_combined = np.concatenate((X, X_valid), axis = 0)
#print(X_combined.shape)
li_valid = np.ones(X_valid.shape[0])
li_valid_color = ['red']*(X_valid.shape[0])


#test
X_test = np.empty((2,1000), int)
f = open('../fb15k/fixedDS/Inductive/Symmetry/People/test2id.txt') 
for line in f.readlines():
    line = line.split()
    if len(line) > 1:
        #print(type(line))
        #head
        h = int(line[0])
        t = int(line[1])
        r = int(line[2])
        h_e = entity_emb_dict[h]
        t_e = entity_emb_dict[t]
        #n = np.concatenate((h_e, t_e), axis=0)        
        n = np.vstack([h_e,t_e])
        #print(n.shape)
        X_test = np.append(X_test, n, axis=0)
print(X_test.shape)
li_test = X_test.shape[0] * [2]
li_color_test = ['orange']*(X_test.shape[0])

#combined the three splits
X_combined = np.concatenate((X, X_valid, X_test), axis = 0)
li_color_combined = np.concatenate((li_color, li_valid_color, li_color_test), axis = 0)
li_combined = np.concatenate((li, li_valid, li_test), axis = 0)
#X_combined = np.concatenate((X, X_test), axis = 0)
#print(X_combined.shape)
X_embedded  = TSNE(n_components=2).fit_transform(X_combined)
#plt.legend()
#plt.show()
fig = plt.figure(figsize=(10,5))
legend_elements = [                   
                   Line2D([0], [0], marker='o', color='b', label='Train',markerfacecolor='b', markersize=10),
                   Line2D([0], [0], marker='o', color='r', label='Valid',markerfacecolor='r', markersize=10),
                   Line2D([0], [0], marker='o', color='orange', label='Test',markerfacecolor='orange', markersize=10)]
ax = fig.add_subplot(111)
ax.legend(handles=legend_elements)
plt.scatter(X_embedded[:,0], X_embedded[:,1], c = li_color_combined, label = li_combined)
plt.show()