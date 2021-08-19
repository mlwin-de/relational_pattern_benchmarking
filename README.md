
The repository includes Benchmarking for KnowledgeGraph link Prediction Task on each specific Relational Pattern and for both inductive and transductive settings.


## 1. Inducive Setting Datasets 

Datasets/WN18_H/Inductive/
Datasets/FB15K_H/Inductive/


## 1.1 Semi-inductive Datasets

### 1.1.1 Semi-Inductive-CountBased

They exist in Datasets/WN18_H/Semi-Inductive-CountBased/
and 
in Datasets/FB15K_H/Semi-Inductive-CountBased/

and each folder includes 4 subfolders for a testing a specific relational pattern: AntiSymmetry, Inference, Symmetry, Inverse.   

### 1.1.2  Semi-Inductive-Semi-Inductive-HeadOrTailBased

They exist in 
/Datasets/WN18_H/Semi-Inductive-HeadOrTailBased/
and 
/Datasets/FB15K_H/Semi-Inductive-HeadOrTailBased/

and each include 4 datasets for each test type: AntiSymmetry, Inference, Symmetry, Inverse.

## 2. Transdictive Setting Dataset
They exist in /Datasets/FB15K_H/Transductive/ folder and /Datasets/WN18_H/Transductive/

and each folder includes 4 subfolders for a testing a specific relational pattern: AntiSymmetry, Inference, Symmetry, Inverse.   


## Code for dataset Generation
Each Test folder includes ".py" files that is used to generate that dataset.  

for example /Datasets/FB15K_H/Semi-Inductive-HeadOrTailBased/inverse/n-n.py is the python script to generate inverese pattern evalation dataset for the semi-inductive that is generated with HeadOrTailBased method. 

