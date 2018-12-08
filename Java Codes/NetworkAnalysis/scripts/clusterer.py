import networkx as nx
import community
import matplotlib.pyplot as plt


graph = nx.karate_club_graph()
partition = community.best_partition(graph)
print(partition)