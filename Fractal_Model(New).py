#coding=utf-8

from math import *
from networkx import *
import random
from copy import deepcopy
import os, sys
import time
import matplotlib.pyplot as plt

def fractal_model(generation,m,x,e):
	'''
	Returns the fractal model introduced by 
	Gallos L K, Song C M, Havlin S and Makse H A in PNAS 2007.
    '''
    G = nx.Graph()
    node_index = 1
    # This is the seed for the network (generation 0)
    for i in range(1,m+1):
        G.add_edge(0, node_index)
        node_index += 1
    if n > m:
        new_nodes = list(G.neighbors(0))
        time_left = int(math.ceil(n / (m-1))) - 1
        node_left = n - m - 1
        for i in range(1,time_left + 1):
            one_of_new_node = new_nodes.pop(0)
            for j in range(1, m):
                if not node_left:
                    break
                G.add_edge(one_of_new_node, node_index)
                new_nodes.append(node_index)
                node_index += 1
                node_left -= 1
    # 产生geration代
    while generation - 1:
        Nt = G.number_of_nodes() * n
        generation -= 1
        # 1.找hub-hub节点
        hub_hub_edges = []
        all_nodes_degree = nx.degree(G)
        hub_nodes = []
        degree_dict = {}
        for item in all_nodes_degree:
            if all_nodes_degree[item] > 2:
                hub_nodes.append(item)
        for source in hub_nodes:
            for target in hub_nodes[hub_nodes.index(source) + 1:]:
                if target in G[source]:
                    hub_hub_edges.append((source, target))
        # 2.满足k(t) = mk(t-1),每个节点加(m-1)k(t-1)条边
        all_edges = list(G.edges())
        new_nodes = {}
        nodes_degree = {}
        for each_node in all_nodes_degree:
            nodes_degree[each_node]=all_nodes_degree[each_node]
            new_nodes[each_node] = set()
            for i in range(1,(m-1)*all_nodes_degree[each_node] + 1):
                G.add_edge(each_node,node_index)
                new_nodes[each_node].add(node_index)
                node_index += 1
        # 排斥hub-hub，断裂节点所有原边除了hub-hub边，重新连接
        break_edges = [edge for edge in all_edges if edge not in hub_hub_edges]
        for edge in break_edges:
            if random.random() > e:
                G.remove_edge(edge[0],edge[1])
                if nodes_degree[edge[0]] > nodes_degree[edge[1]]:
                    G.add_edge(edge[0],new_nodes[edge[1]].pop())
                else:
                    G.add_edge(edge[1], new_nodes[edge[0]].pop())
        # 一个新节点排斥hub-hub节点
        for edge in hub_hub_edges:
            if node_index >= Nt:
                break
            if random.random() > e:
                G.remove_edge(edge[0], edge[1])
                G.add_edge(edge[0],node_index)
                G.add_edge(edge[1],node_index)
                node_index += 1
        # 随机连接节点知道满足Nt为止
        all_nodes_degree = nx.degree(G)
        ran_nodes = []
        for item in all_nodes_degree:
            if all_nodes_degree[item] > 1:
                ran_nodes.append(all_nodes_degree[item])
        node_max = node_index - 1
        for i in range(1,Nt - G.number_of_nodes() + 1):
            #G.add_edge(random.choice(ran_nodes),node_index)
            G.add_edge(random.randint(1,node_max),node_index)
            node_index += 1
    return G

if __name__ == '__main__':
	
	g = fractal_model(3,6,3,0)
	print ("网络节点总数为%d"%g.number_of_nodes())
	print ("网络直径为%d"%nx.diameter(g))