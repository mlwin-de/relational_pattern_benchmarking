
The repository includes Benchmarking for KnowledgeGraph link Prediction Task on each specific Relational Pattern and for both inductive and transductive settings.
The content includes





The details of the studied datasets:


|                                | Dataset Variant  | Type            | Total Entities | Total Relations | Nodes In Graph | Edges In Graph | Avg Degree Of Graph | Dimension Of Graph | Strongly Connected Components |
| ------------------- | ----------- | ----------- | ------------ | ---------- | ----------- | ----------- | ---------- | --------- | ---------- |
|                                |                 |                 |                 |                  |              |              |                  |                  |                             |
| FB15K                          | Transductive    | Symmetry /People | 1044            | 3                | 1044         | 2508         | 4                | 2508             | 142                         |
| Transductive                   | inverse         | 8005            | 626             | 8005             | 26457        | 6            | 26457            | 224              |
| Transductive                   | AntiSymmetry    | 8005            | 529             | 8005             | 13277        | 3            | 13277            | 5050             |
| Transductive                   | Inference       | 1337            | 102             | 1337             | 1072         | 1            | 1072             | 1313             |
| Inductive                      | Symmetry/People | 1062            | 3               | 1062             | 2066         | 3            | 2066             | 328              |
| Inductive                      | inverse         | 8614            | 626             | 8614             | 20256        | 4            | 20256            | 778              |
| Inductive                      | AntiSymmetry    | 8539            | 529             | 8539             | 10102        | 2            | 10102            | 7247             |
| Inductive                      | Inference       | 1413            | 102             | 1413             | 1065         | 1            | 1065             | 1397             |
| Semi-Inductive-CountBased      | Symmetry/People | 1062            | 3               | 1062             | 2084         | 3            | 2084             | 319              |
| Semi-Inductive-CountBased      | inverse         | 8614            | 626             | 8614             | 20907        | 4            | 20907            | 740              |
| Semi-Inductive-CountBased      | AntiSymmetry    | 8539            | 529             | 8539             | 10407        | 2            | 10407            | 7117             |
| Semi-Inductive-CountBased      | Inference       | 1413            | 102             | 1413             | 1110         | 1            | 1110             | 1389             |
| Semi-Inductive-HeadOrTailBased | Symmetry/People | 1053            | 3               | 1053             | 2066         | 3            | 2066             | 319              |
| Semi-Inductive-HeadOrTailBased | inverse         | 9643            | 626             | 9643             | 23799        | 4            | 23799            | 456              |
| Semi-Inductive-HeadOrTailBased | AntiSymmetry    | 9605            | 529             | 9605             | 11870        | 2            | 11870            | 8122             |
| Semi-Inductive-HeadOrTailBased | Inference       | 1423            | 102             | 1423             | 1110         | 1            | 1110             | 1407             |
| WN18                           | Transductive    | Symmetry        | 16975           | 3                | 16975        | 33268        | 3                | 33268            | 2600                        |
| Transductive                   | inverse         | 12748           | 18              | 12748            | 18117        | 2            | 18117            | 3729             |
| Transductive                   | AntiSymmetry    | 12748           | 18              | 12748            | 9058         | 1            | 9058             | 12732            |
| Transductive                   | Inference       | 11549           | 14              | 11549            | 17371        | 3            | 17371            | 2931             |
| Inductive                      | Symmetry        | 16991           | 3               | 16991            | 31110        | 3            | 31110            | 3977             |
| Inductive                      | inverse         | 13130           | 18              | 13130            | 18287        | 2            | 18287            | 4019             |
| Inductive                      | AntiSymmetry    | 13129           | 18              | 13129            | 9143         | 1            | 9143             | 13117            |
| Inductive                      | Inference       | 13213           | 14              | 13213            | 18327        | 2            | 18327            | 4080             |
| Semi-Inductive-CountBased      | Symmetry        | 16991           | 3               | 16991            | 31126        | 3            | 31126            | 3962             |
| Semi-Inductive-CountBased      | inverse         | 13130           | 18              | 13130            | 18502        | 2            | 18502            | 3919             |
| Semi-Inductive-CountBased      | AntiSymmetry    | 13129           | 18              | 13129            | 9250         | 1            | 9250             | 13113            |
| Semi-Inductive-CountBased      | Inference       | 13213           | 14              | 13213            | 19151        | 2            | 19151            | 3705             |
| Semi-Inductive-HeadOrTailBased | Symmetry        | 17012           | 3               | 17012            | 31159        | 3            | 31159            | 3977             |
| Semi-Inductive-HeadOrTailBased | inverse         | 13121           | 18              | 13121            | 18652        | 2            | 18652            | 3828             |
| Semi-Inductive-HeadOrTailBased | AntiSymmetry    | 13121           | 18              | 13121            | 9326         | 1            | 9326             | 13109            |
| Semi-Inductive-HeadOrTailBased | Inference       | 13362           | 14              | 13362            | 20217        | 3            | 20217            | 3285             |





The following is index as:

1. Inductive Setting Datasets 
2. Transductive Setting Dataset
3. Train Hyperparamters 
4. Installation

## 1. Inductive Setting Datasets 

The path to induction setting datasets:

``Datasets/WN18_H/Inductive/``
``Datasets/FB15K_H/Inductive/``


## 1.1 Semi-inductive Datasets

### 1.1.1 Semi-Inductive-CountBased

They exist in ``Datasets/WN18_H/Semi-Inductive-CountBased/``
and 
in ``Datasets/FB15K_H/Semi-Inductive-CountBased/``

and each folder includes 4 subfolders for a testing a specific relational pattern: AntiSymmetry, Inference, Symmetry, Inverse.   

### 1.1.2  Semi-Inductive-Semi-Inductive-HeadOrTailBased

They exist in 
``/Datasets/WN18_H/Semi-Inductive-HeadOrTailBased/``
and 
``/Datasets/FB15K_H/Semi-Inductive-HeadOrTailBased/``

and each include 4 datasets for each test type: AntiSymmetry, Inference, Symmetry, Inverse.

## 2. Transductive Setting Dataset
They exist in ``/Datasets/FB15K_H/Transductive/`` folder and ``/Datasets/WN18_H/Transductive/``

and each folder includes 4 subfolders for a testing a specific relational pattern: AntiSymmetry, Inference, Symmetry, Inverse.   


## Code for dataset Generation
The code for generating the dataset consist of several ".py" python scripts in the folder "/utils".  

For example python ``/utils/anti-symm-extractor-fb15k.py`` command generates anti symmetric pattern dataset for fb15k dataset.


## 3. Train Hyperparamters 
The train Hyperparamters and commands used to train each model is listed in hyperparams.txt

## 4. Installation & Usage

First make sure that you have all requirements installed.
###  Requirements
- `networkx`
- `numpy` 
- `Python` 3.x
- `scipy` (somewhat recent version)
- `sklearn` (somewhat recent version)
- `torch` 1.5

## Usage
See ``https://github.com/mlwin-de/relational_pattern_benchmarking/blob/master/utils/relationalpatterns.py`` for generation of datasets and and ``https://github.com/mlwin-de/relational_pattern_benchmarking/blob/master/hyperparams.txt`` for evaluation examples. 

