
The repository includes Benchmarking for KnowledgeGraph link Prediction Task on each specific Relational Pattern and for both inductive and transductive settings.
The content includes

1. Inductive Setting Datasets 
2. Transductive Setting Dataset
3. Train Hyperparamters 

## 1. Inductive Setting Datasets 

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

## 2. Transductive Setting Dataset
They exist in /Datasets/FB15K_H/Transductive/ folder and /Datasets/WN18_H/Transductive/

and each folder includes 4 subfolders for a testing a specific relational pattern: AntiSymmetry, Inference, Symmetry, Inverse.   


## Code for dataset Generation
The code for generating the dataset consist of several ".py" python scripts in the folder "/utils".  

For example python /utils/anti-symm-extractor-fb15k.py command generates anti symmetric pattern dataset for fb15k dataset.


## 3. Train Hyperparamters 
The train Hyperparamters and commands used to train each model is listed in hyperparams.txt
