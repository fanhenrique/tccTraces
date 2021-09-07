import numpy as np
import matplotlib.pyplot as plt

import networkx as nx

#my imports
import var

def draw_graph(graph):

	colors = [u[1] for u in graph.nodes(data='color_nodes')]
	# nx.draw(graph, with_labels=True, node_color=colors)
	
	pos = nx.spring_layout(graph)
	# pos = nx.drawing.nx_agraph.graphviz_layout(graph, prog='dot')
	weights = nx.get_edge_attributes(graph, "weight")

	nx.draw_networkx(graph, pos, with_labels=True, node_color=colors)
	nx.draw_networkx_edge_labels(graph, pos, edge_labels=weights)

def show_graph(graph):

	draw_graph(graph)
	
	plt.show()

def save_graph_fig(graph, g):

	draw_graph(graph)
		
	plt.savefig(var.PATH_FIGS+'/graph'+str(g)+'.png')
	plt.clf()

def save_graph_txt(graph, g):
	# print(graph.nodes.data())
	with open(var.PATH_GRAPHS+'/graph'+str(g)+'.txt', 'w') as file:
		for edge in graph.edges.data():
			if edge[2]:
				file.write(edge[0] + ' ' + str(edge[2]['weight']) + ' ' + edge[1] + '\n')
			else:
				file.write(edge[0] + ' ' + edge[1] + '\n')

def entities(monitors, trackers, peer_lists):

	monitor_list = list(dict.fromkeys(monitors))
	tracker_list = list(dict.fromkeys(trackers))
	pls = []
	for pl in peer_lists:
		for p in pl:
			pls.append(p)
	p_list = list(dict.fromkeys(pls))

	vector = []

	if var.SHOWMASTER:
		vector.append('MS')

	vector += monitor_list + tracker_list

	if var.SHOWPEERS:
		vector += p_list

	return vector, monitor_list, tracker_list, p_list


def save_graph_adj_csv(graphs, monitors, trackers, peer_lists):

	vector, monitor_list, tracker_list, p_list = entities(monitors, trackers, peer_lists)

	print(vector, len(vector))

	matrix = np.zeros((len(vector), len(vector)), dtype=int)

	if var.SHOWMASTER:
		for m in monitor_list:
			matrix[0,vector.index(m)] = 1
			matrix[vector.index(m), 0] = 1

	for m in monitor_list:
		for t in tracker_list:
			matrix[vector.index(m), vector.index(t)] = 1
			matrix[vector.index(t),vector.index(m)] = 1
	
	if var.SHOWPEERS:
		for t in tracker_list:
			for pl in p_list:
				matrix[vector.index(t),vector.index(pl)] = 1
				matrix[vector.index(pl),vector.index(t)] = 1

	with open(var.PATH_MATRICES+'/monitoring_adj.csv', 'w') as file:				

		for i in range(matrix.shape[0]):
			for j in range(matrix.shape[1]):
				file.write(str(matrix[i,j])+'\n') if j == matrix.shape[1]-1 else file.write(str(matrix[i,j])+',')

def save_graph_weigths_csv(graphs, monitors, trackers, peer_lists):

	vector, _ , _, _ = entities(monitors, trackers, peer_lists)			

	with open(var.PATH+'/out_matrices/monitoring_weigths.csv', 'w') as file:
		for g in graphs:

			matrix = np.zeros((len(vector), len(vector)), dtype=int)

			for e in g.edges().data():

				matrix[vector.index(e[0]), vector.index(e[1])] = e[2]['weight']
				matrix[vector.index(e[1]), vector.index(e[0])] = e[2]['weight']

			for i in range(matrix.shape[0]):
				for j in range(matrix.shape[1]):
					file.write(str(matrix[i,j])+'\n') if j == matrix.shape[1]-1 else file.write(str(matrix[i,j])+',')