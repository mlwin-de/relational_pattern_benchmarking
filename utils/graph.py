import networkx as nx
import matplotlib.pyplot as plt
import csv
dataset = '../wn18'
#, 'Inductive', 'Semi-Inductive-CountBased', 'Semi-Inductive-HeadOrTailBased'
#,'valid','test'
#,'inverse','AntiSymmetry', 'Inference'
datasetVariant = ['Transductive', 'Inductive', 'Semi-Inductive-CountBased', 'Semi-Inductive-HeadOrTailBased']
type = ['Symmetry','inverse','AntiSymmetry', 'Inference']
filetype = ['train','valid','test']
output_str = ''
entities = []
relations = []
all_lines = []
field_names = ['datasetVariant','type','total_Entities', 'total_Relations', 'NodesInGraph','edgesInGraph','AvgDegreeOfGraph','dimOfGraph','stronglyConnectedComponents']
with open(dataset + '/GraphResults.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    for t in datasetVariant:    
        output_str += '\n'+ t + '\n'
        for ty in type:
            output_str += '\n' + ty + '\n' 
            entities.clear()
            relations.clear()
            all_lines.clear()
            for f_type in filetype:               
                output_str += f_type + '\n'
                f = open(dataset+'/fixedDS/'+t+'/'+ty+'/'+ f_type +'.txt') 
                lines = f.readlines()
                i = 0
                for line in lines:
                    l = line.split()
                    l[2] = l[2].rstrip()
                    if(l[0] not in entities):
                        entities.append(l[0])
                    if l[2] not in entities:
                        entities.append(l[2])
                    if l[1] not in relations:
                        relations.append(l[1])
                    all_lines.append(line)
                #for l in entities:
                #    G.add_node(l)
            G=nx.DiGraph()
            for l in all_lines:
                li = l.split()
                li[2] = li[2].rstrip()    
                G.add_edge(li[0], li[2])
            output_str += 'total unique entities ' + str(len(entities)) + '\n'
            print('total unique entities ', len(entities))
            print('total unique relations ', len(relations))
            output_str += 'total unique relations ' + str(len(relations)) + '\n'
            print('nodes in graph ', len(G.nodes()))
            print('edges in graph ', len(G.edges()))
            output_str += 'nodes in graph ' + str(len(G.nodes())) + '\n' 
            output_str += 'edges in graph ' + str(len(G.edges())) + '\n'
            degrees = G.degree()
            #print(degrees)
            degree_values = dict(degrees).values()
            #print(degree_values)
            sum_of_edges = sum(degree_values)
            #degree of graph
            degree_of_graph = sum_of_edges//float(len(G))
            print('average degree of graph ', degree_of_graph)
            output_str += 'average degree of graph ' + str(degree_of_graph) + '\n'
            #dimension
            print('dimension of graph', G.size())
            output_str += 'dimension of graph ' + str(G.size()) + '\n'
            #connected components 
            #print('connected components ', nx.number_connected_components(G))
            print('strongly connected components ', nx.number_strongly_connected_components(G))
            output_str += 'strongly connected components ' + str(nx.number_strongly_connected_components(G)) + '\n' + '\n'
            #'datasetVariant','type','total_Entities', 'total_Relations', 'NodesInGraph','edgesInGraph','AvgDegreeOfGraph','dimOfGraph','stronglyConnectedComponents'
            writer.writerow({'datasetVariant' : t, 'type' : ty, 'total_Entities' : len(entities), 'total_Relations': len(relations), 
            'NodesInGraph' : len(G.nodes()), 'edgesInGraph' :len(G.edges()), 'AvgDegreeOfGraph':degree_of_graph, 'dimOfGraph': G.size(), 'stronglyConnectedComponents':nx.number_strongly_connected_components(G)})
            #print(sum_of_edges)
            #pos = nx.draw_spring(G)
            #nx.draw_networkx_labels(G, pos)
            #nx.draw_networkx_edges(G, pos, arrows=False)
            #plt.show()

            #print(len(all_lines))
f2 = open(dataset+'/GraphResults.txt', 'w')
f2.write(output_str)  