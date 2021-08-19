# relational_pattern_benchmarking_datasets
The repository includes Benchmarking for KnowledgeGraph link Prediction Task on each specific Relational Pattern and for both inductive and transductive settings.


## Inducive Setting Datasets 

Datasets/WN18_H/Inductive/
Datasets/FB15K_H/Inductive/


## Semi-inductive Datasets

### Semi-Inductive-CountBased

### Semi-Inductive-Semi-Inductive-HeadOrTailBased

They exist in 
/Datasets/WN18_H/Semi-Inductive-HeadOrTailBased/
and 
/Datasets/FB15K_H/Semi-Inductive-HeadOrTailBased/

and each include 4 datasets for each test type: AntiSymmetry, Inference, Symmetry, inverse 

## Transdictive Setting Dataset
Inductive

## Code for dataset Generation
Each Test folder includes ".py" files that is used to generate that dataset.  

for example /Datasets/FB15K_H/Semi-Inductive-HeadOrTailBased/inverse/n-n.py is the python script to generate inverese pattern evalation dataset for the semi-inductive that is generated with HeadOrTailBased method. 

