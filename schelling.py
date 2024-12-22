import networkx as nx
import matplotlib.pyplot as plt
import random

# grid size
# N = 10
N = int(input("Enter dimension of grid: "))
t = int(input("Enter the Threshold value: "))

# init graph
G = nx.grid_2d_graph(N, N)

# arrange grid and assign labels
pos = dict((n,n) for n in G.nodes())
labels = dict(((i,j), i*N+j) for i,j in G.nodes())

# add diagonal links
for(u,v) in G.nodes():
    if(u+1 <= N-1) and (v+1 <= N-1):
        G.add_edge((u,v),(u+1,v+1))

for(u,v) in G.nodes():
    if(u+1 <= N-1) and (v-1 >= 0):
        G.add_edge((u,v),(u+1,v-1))

"""assign attribute type to every node
    type 0: empty node
    type 1: person of type 1
    type 2: person of type 2"""
for n in G.nodes():
    G._node[n]['type'] = random.randint(0,2)

# maintaining lists of occupants
empty_cells = [n for (n,d) in G.nodes(data = True) if d['type'] == 0]
type1_nodes_list = [n for (n,d) in G.nodes(data = True) if d['type'] == 1]
type2_nodes_list = [n for (n,d) in G.nodes(data = True) if d['type'] == 2]

# graph decorator and plotter
def display_graph(G):
    """ empty nodes: white
        type1 nodes: green
        type2 nodes: red"""
    nodes_g = nx.draw_networkx_nodes(G, pos, node_color = 'green', nodelist = type1_nodes_list)
    nodes_r = nx.draw_networkx_nodes(G, pos, node_color = 'red', nodelist = type2_nodes_list)
    nodes_w = nx.draw_networkx_nodes(G, pos, node_color = 'white', nodelist = empty_cells)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, labels = labels)
    plt.show()

def get_boundary_nodes(G):
    boundary_nodes_list = []
    for ((u,v),d) in G.nodes(data = True):
        if u==0 or u==N-1 or v==0 or v==N-1:
            boundary_nodes_list.append((u,v))
    return boundary_nodes_list

boundary_nodes_list = get_boundary_nodes(G)
internal_nodes_list = list(set(G.nodes()) - set(boundary_nodes_list))

def get_neighbour_for_internal(u,v):
    return[(u-1, v), (u+1, v), (u, v-1), (u, v+1), (u-1, v+1), (u+1, v-1), (u-1, v-1), (u+1, v+1)]

def get_neighbour_for_boundary(u,v):
    if u ==0 and v==0:
        return [(0,1),(1,1),(1,0)]
    elif u==N-1 and v==N-1:
        return[(N-2,N-2),(N-1,N-2),(N-2,N-1)]
    elif u==N-1 and v==0:
        return[(u-1,v),(u,v+1),(u-1,v+1)]
    elif u==0 and v==N-1:
        return[(u+1,v),(u+1,v-1),(u,v-1)]
    elif u==0:
        return[(u,v-1),(u,v+1),(u+1,v),(u+1,v-1),(u+1,v+1)]
    elif u==N-1:
        return[(u-1,v),(u,v-1),(u,v+1),(u-1,v+1),(u-1,v-1)]
    elif v==N-1:
        return[(u,v-1),(u-1,v),(u+1,v),(u-1,v-1),(u+1,v-1)]
    elif v==0:
        return[(u-1,v),(u+1,v),(u,v+1),(u-1,v+1),(u+1,v+1)]
    
def get_unsatisfied_nodes_list(G,boundary_nodes_list,internal_nodes_list):
    unsatisfied_nodes_list = []
    # t = 3
    for u,v in G.nodes():
        type_of_this_node = G._node[(u,v)]['type']
        if type_of_this_node == 0:
            continue
        else:
            similar_nodes = 0
            if (u,v) in internal_nodes_list:
                neigh = get_neighbour_for_internal(u,v)
            elif (u,v) in boundary_nodes_list:
                neigh = get_neighbour_for_boundary(u,v)

            for each in neigh:
                if G._node[each]['type'] == type_of_this_node:
                    similar_nodes += 1

            if similar_nodes <= t:
                unsatisfied_nodes_list.append((u,v))

    return unsatisfied_nodes_list


def make_a_node_satisfied(unsatisfied_nodes_list, empty_cells):
    if(len(unsatisfied_nodes_list)!=0):
        node_to_shift = random.choice(unsatisfied_nodes_list)
        new_position = random.choice(empty_cells)

        G._node[new_position]['type'] = G._node[node_to_shift]['type']
        G._node[node_to_shift]['type'] = 0

        labels[node_to_shift], labels[new_position] = labels[new_position], labels[node_to_shift]
    
    else:
        print('all nodes satisfied')

display_graph(G)

for i in range(5000):
    unsatisfied_nodes_list = get_unsatisfied_nodes_list(G,boundary_nodes_list,internal_nodes_list)

    make_a_node_satisfied(unsatisfied_nodes_list,empty_cells)
    empty_cells = [n for (n,d) in G.nodes(data = True) if d['type'] == 0]
    type1_nodes_list = [n for (n,d) in G.nodes(data = True) if d['type'] == 1]
    type2_nodes_list = [n for (n,d) in G.nodes(data = True) if d['type'] == 2]

    if(i%1000 == 0):
        display_graph(G)