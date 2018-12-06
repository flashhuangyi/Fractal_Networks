#coding=utf-8

from math import *
from networkx import *
import random
from copy import deepcopy
import os, sys
import time
import matplotlib.pyplot as plt

def fractal_model(generation,m,x,e):
	"""
	Returns the fractal model introduced by 
	Song, Havlin, Makse in Nature Physics 2, 275.
	generation = number of generations
	m = number of offspring per node
	x = number of connections between offsprings
	e = probability that hubs stay connected
	1-e = probability that x offsprings connect.
	If e=1 we are in MODE 1 (pure small-world).
	If e=0 we are in MODE 2 (pure fractal).
	"""
	G=Graph()
	G.add_edge(0,1) #This is the seed for the network (generation 0)
	node_index = 2
	for n in range(1,generation+1):
		all_links = G.edges()
		while all_links:
			link = all_links.pop()
			new_nodes_a = range(node_index,node_index + m)
			#random.shuffle(new_nodes_a)
			node_index += m
			new_nodes_b = range(node_index,node_index + m)
			#random.shuffle(new_nodes_b)
			node_index += m
			G.add_edges_from([(link[0],node) for node in new_nodes_a])
			G.add_edges_from([(link[1],node) for node in new_nodes_b])
			repulsive_links = zip(new_nodes_a,new_nodes_b)
			G.add_edges_from([repulsive_links.pop() for i in range(x-1)])
			if random.random() > e:
				G.remove_edge(*(link))
				G.add_edge(*(repulsive_links.pop()))
	return G

def random_box_covering(G,rb):
	"""
	It returns a dictionary with {box_id:subgraph_generated_by_the_nodes_in_this_box}
	The box_id is the center of the box.
	"""
	H = deepcopy(G)
	burned_nodes = []
	unburned_nodes = G.nodes()
	boxes_subgraphs = {}
	adj = H.adj
	while unburned_nodes:
		center_node = random.choice(unburned_nodes) 
		nodes_visited = [center_node]
		search_queue = [center_node]
		d = 1
		while search_queue and d <= rb:
			next_depth = []
			extend = next_depth.extend
			for n in search_queue:
				l = [ i for i in adj[n].iterkeys() if i not in nodes_visited]
				extend(l)
				nodes_visited.extend(l)
			search_queue = next_depth
			d += 1
		new_burned_nodes = nodes_visited#.keys()
		H.delete_nodes_from(new_burned_nodes)
		boxes_subgraphs[center_node] = subgraph(G,new_burned_nodes)
		unburned_nodes = list(set(unburned_nodes)-set(new_burned_nodes))
	return boxes_subgraphs

if __name__ == '__main__':

	g = fractal_model(3,6,3,0)
	print ("网络节点总数为%d"%g.number_of_nodes())
	print ("网络直径为%d"%nx.diameter(g))
	boxes_subgraphs = random_box_covering(g,1)
	print boxes_subgraphs

	